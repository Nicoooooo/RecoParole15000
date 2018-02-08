from collections import defaultdict

psub = 0
pins = 0
pomi = 0
matrix = defaultdict(dict)

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

def tester_mot(mot, fileUrl) :
    file = open(fileUrl, "r")
    m = mot.strip().split(" ")

    for line in file:
        splt = line.replace("\n", " ").split("\t")
        phonetique = (splt[1]).strip().split(" ")

        print(splt[0] + " [" + splt[1] + "] => " + str(levenshtein(m, phonetique)))


def ouvrir_HMM(hmm):
    file = open(hmm, "r")
    file.readline()
    line = file.readline().split(";")
    psub = float(line[0])
    pins = float(line[1])
    pomi = float(line[2])
    file.readline()
    indices = file.readline().replace("\n", "").split(";")

    for i in range(34):
        line = file.readline().replace("\n", "").split(";")
        print(line)
        for j in range(33):
            matrix[line[0]][indices[j+1]] = float(line[j+1])


ouvrir_HMM("data/modele_discret_initialise.dat")