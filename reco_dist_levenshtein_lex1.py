import sys
from termcolor import colored, cprint

#text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
#print(text)
#cprint('Hello')

def levenshtein(seq1, seq2):
    oneago = None
    thisrow = list(range(1, len(seq2) + 1)) + [0]
    for x in range(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in range(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]

def alignement(seq1, seq2):
    res = ""

    while len(seq1) < len(seq2):
        seq1 = seq1 + " "
    while len(seq2) < len(seq1):
        seq2 = seq2 + " "

    for x in range(len(seq1)):
        if seq1[x] != " ":
            res = res + "(" + seq1[x] + "=>" + seq2[x] + ") "
    return res

def recuperer_meilleur_match(motReel, mot, fileUrl):
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
        print("  - " + motReel + " [" + mot + "] => " + motTrouve + " [" + motTrouvePhonetique + "] CORRECT (d=" + str(mini) + ") ")
        return 0
    else:
        print(colored("  - " + motReel + " [" + mot + "] => " + motTrouve + " [" + motTrouvePhonetique + "] ERREUR (d=" + str(mini) + ") " + alignement(mot, motTrouvePhonetique), 'red', attrs=['bold']))
        return 1

def tester_lexique(lexiqueUrl, testUrl):
    print("Test (lexique = " + lexiqueUrl + ", test = " + testUrl)

    cnt = 0
    err = 0

    lex = open(lexiqueUrl, "r")
    for line in lex:
        cnt += 1
        splt = line.replace("\n", " ").split("\t")
        test = recuperer_meilleur_match(splt[0], splt[1], testUrl)
        if test == 1:
            err += 1

    print("Résultats : " + str(cnt - err) + "/" + str(cnt) + " bons résultats (" + str( round(((cnt-err)/cnt)*100) ) + "%)")

#print(alignement("j z i l", "O s i"))
tester_lexique("data/test-3syll-0100words.test", "data/lexicon-3syll-0500words.lex")
