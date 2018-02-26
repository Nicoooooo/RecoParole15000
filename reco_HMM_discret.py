from collections import defaultdict

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



ouvrir_HMM("data/modele_discret_initialise.dat")
print(matrix)
print(insertion)