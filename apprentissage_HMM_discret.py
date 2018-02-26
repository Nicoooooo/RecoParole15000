from collections import defaultdict

psub = 0.0
pins = 0.0
pomi = 0.0
matrix = defaultdict(dict)
indices = ["2","9","@","e","E","o","O","a","i","u","y","a~","o~","e~","H","w","j","R","l","p","t","k","b","d","g","f","s","S","v","z","Z","m","n","J"]
insertion = [0]*len(indices)

def init():
    global matrix
    for i in range (len(indices)):
        for j in range(len(indices)):
            matrix[indices[i]][indices[j]] = 0

def alignment(seq1, seq2):
    res = ""

    while len(seq1) < len(seq2):
        seq1 = seq1 + " "
    while len(seq2) < len(seq1):
        seq2 = seq2 + " "

    for x in range(len(seq1)):
        if seq1[x] != " ":
            res = res + "(" + seq1[x] + "=>" + seq2[x] + ") "
    return res


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

init()
apprentissage("data/train-01000items.train")
enregistrer_HMM("iter1.dat")