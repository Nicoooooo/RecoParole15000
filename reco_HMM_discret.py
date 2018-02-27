from collections import defaultdict
import sys
import difflib
from termcolor import colored, cprint
import math

psub = 0
pins = 0
pomi = 0
matrix = defaultdict(dict) # matrix[ref][test]
indices = ["2","9","@","e","E","o","O","a","i","u","y","a~","o~","e~","H","w","j","R","l","p","t","k","b","d","g","f","s","S","v","z","Z","m","n","J"]
insertion = defaultdict(dict)

def ouvrir_HMM(hmm):
    global psub, pins, pomi, matrix, indices, insertion
    file = open(hmm, "r")
    file.readline()
    line = file.readline().split(";")
    psub = float(line[0])
    pins = float(line[1])
    pomi = float(line[2])

    file.readline()
    file.readline()

    for i in range(len(indices)):
        line = file.readline().replace("\n", "").split(";")
        for j in range(len(indices)):
            matrix[indices[i]][indices[j]] = float(line[j+1])

    file.readline()
    line = file.readline().replace("\n", "").split(";")
    for i in range(len(indices)):
        insertion[indices[i]] = float(line[i+1])



def levenshtein(seq1, seq2):
    oneago = None
    thisrow = list(range(1, len(seq2) + 1)) + [0]
    for x in range(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in range(len(seq2)):
            delcost = oneago[y] - math.log(pomi)
            addcost = thisrow[y - 1] - math.log(pins) - math.log(float(insertion[seq1[x]]))
            subcost = oneago[y - 1] - math.log(psub) - math.log(float(matrix[seq1[x]][seq2[y]]))
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]


def alignment(seq1, seq2):
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
                    last = ""
                elif last == '-': # sortie valeur précédente
                    res += '({} => \"\") '.format(sub,sub)
                    last = '-'
                    sub = s[-1]
                else: # en mémoire
                    last = '-'
                    sub = s[-1]
            elif s[0]=='+':
                if last == '+': # sortie valeur précédente
                    res += '(\"\" => {}) '.format(sub,sub)
                    last = '+'
                    sub = s[-1]
                elif last == '-': # substitution
                    res += '({} => {}) '.format(sub,s[-1])
                    last = ""
                else: # en mémoire
                    last = '+'
                    sub = s[-1]

    return res


def best_match(motReel, mot, fileUrl):
    file = open(fileUrl, "r")
    m = mot.strip().split(" ")

    mini = 999999999
    motTrouve = ""
    motTrouvePhonetique = ""

    for line in file:
        splt = line.replace("\n", " ").split("\t")
        phonetique = (splt[1]).strip().split(" ")

        if levenshtein(m, phonetique) < mini:
            mini = levenshtein(m, phonetique)
            motTrouve = splt[0]
            motTrouvePhonetique = splt[1]

    if motTrouve == motReel or motTrouve + 's' == motReel or motTrouve == motReel + 's':
        print("  - " + motReel + " [" + mot + "] => " + motTrouve + " [" + motTrouvePhonetique + "] CORRECT (d=" + str(mini) + ") " + alignment(mot, motTrouvePhonetique))
        return 0
    else:
        print(colored("  - " + motReel + " [" + mot + "] => " + motTrouve + " [" + motTrouvePhonetique + "] ERREUR (d=" + str(mini) + ") " + alignment(mot, motTrouvePhonetique), 'red', attrs=['bold']))
        return 1


def test_lexicon(lexiqueUrl, testUrl):
    print("Test (lexique = " + lexiqueUrl + ", test = " + testUrl)

    cnt = 0
    err = 0

    lex = open(lexiqueUrl, "r")
    for line in lex:
        cnt += 1
        splt = line.replace("\n", " ").split("\t")
        test = best_match(splt[0], splt[1], testUrl)
        if test == 1:
            err += 1

    print("Résultats : " + str(cnt - err) + "/" + str(cnt) + " bons résultats (" + str( round(((cnt-err)/cnt)*100) ) + "%)")


ouvrir_HMM("data/modele_discret_initialise.dat")
test_lexicon("data/test-3syll-0100words.test", "data/lexicon-3syll-0500words.lex")