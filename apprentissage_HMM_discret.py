from collections import defaultdict
import difflib

psub = 0.0
pins = 0.0
pomi = 0.0
matrix = defaultdict(dict)
indices = ["2","9","@","e","E","o","O","a","i","u","y","a~","o~","e~","H","w","j","R","l","p","t","k","b","d","g","f","s","S","v","z","Z","m","n","J"]
insertion = defaultdict(dict)

def init():
    global psub, pins, pomi, matrix, insertion
    psub = 0.0
    pins = 0.0
    pomi = 0.0
    for i in range (len(indices)):
        insertion[indices[i]] = 0
        for j in range(len(indices)):
            matrix[indices[i]][indices[j]] = 0

def apprentissage(app):
    with open(app, 'r') as f:
        for line in f:
            elem = line.replace("\n", "").replace("[","").replace("]","").replace(" ","").split("\t")
            ali = alignment(elem[1], elem[2])
            print(ali)
        else:
            print("end")



def enregistrer_HMM(hmm):
    global psub, pins, pomi, matrix, indices, insertion
    file = open(hmm, "w")
    file.write("Psub;Pins;Pomi\n")
    file.write(str('%.3f' % psub)+";"+str('%.3f' % pins)+";"+str('%.3f' % pomi)+"\n")
    file.write("#Une ligne par symbole de reference; une colonne par symbole de test\n")

    file.write("  ")
    for i in range (len(indices)):
        file.write(';'+indices[i])
    file.write("\n")

    for i in range (len(indices)):
        file.write(indices[i])
        for j in range(len(indices)):
            file.write(';'+str('%.3f' % matrix[indices[i]][indices[j]]))
        file.write("\n")

    file.write("Proba insertions...\n")
    file.write("<ins>")
    for i in range (len(insertion)):
        file.write(';'+str('%.3f' % insertion[i]))
    file.write("\n")

def alignment(seq1, seq2):
    global psub, pins, pomi, matrix, insertion

    res = ""
    sub = ""
    last = ""

    for i,s in enumerate(difflib.ndiff(seq1, seq2)):
        if s[-1] != ' ' and s[-1] != '':
            if s[0] == ' ':
                res += '({} => {}) '.format(s[-1],s[-1])
            elif s[0] == '-':
                if last == '+': # substitution
                    res += '({} => {}) '.format(sub,s[-1])
                    # matrix[i-1][i] = matrix[i-1][i] + 1
                    psub += 1
                    last = ""
                elif last == '-': # sortie valeur précédente
                    res += '({} => \"\") '.format(sub,sub)
                    last = '-'
                    sub = s[-1]
                    pomi += 1
                else: # en mémoire
                    last = '-'
                    sub = s[-1]
            elif s[0]=='+':
                if last == '+': # sortie valeur précédente
                    res += '(\"\" => {}) '.format(sub,sub)
                    last = '+'
                    sub = s[-1]
                    pins += 1
                    # insertion[i] = (insertion[i] + 1)
                elif last == '-': # substitution
                    res += '({} => {}) '.format(sub,s[-1])
                    last = ""
                    # matrix[i][i-1] += matrix[i][i-1] + 1
                    psub += 1
                else: # en mémoire
                    last = '+'
                    sub = s[-1]

    return res

init()
apprentissage("data/train-01000items.train")
enregistrer_HMM("iter1.dat")