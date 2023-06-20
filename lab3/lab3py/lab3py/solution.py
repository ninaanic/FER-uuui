import re
import sys
from decisiontree import getInputData, DecisionTree, getPrediction

args = sys.argv
trainSetPath = args[1]
testSetPath = args[2]

ima = 0
try: 
    dubinaZaPoredzivanje = args[3]
    ima = 1
except:
    ima = 0

D, X, y, featureValues = getInputData(trainSetPath)
tree = DecisionTree(D, X, y) # init new decision tree 
tree.ID3init()  # call ID3init which calls ID3 alg
treeInList = tree.displayTreeInit() # display tree


if ima:
    # ispis [BRANCHES]:
    print("[BRANCHES]: ")
    listOfLists = []
    for lista in treeInList:
        i = 1
        pomocna = []
        for j in range(0, len(lista)-1, 2):
            if i <= int(dubinaZaPoredzivanje):
                pomocna.append(str(i) + ':' + lista[j] + '=' + lista[j+1][:-1])
            i += 1

        # predictaj za one koje smo odrezali 
        if i > int(dubinaZaPoredzivanje)+1:
            prediction = getPrediction(D, X, pomocna)
            pomocna.append(prediction)
        else:
            pomocna.append(lista[-1])

        nemojDodat = 0
        for l in listOfLists:
            if pomocna[:-1] == l[:-1]:
                nemojDodat = 1
        if nemojDodat == 0:
            listOfLists.append(pomocna)
            print(' '.join(pomocna))
    #print(listOfLists)

    listOfDict = [] # trebat ce nam kasnije za accuracy i predictions
    for lista in listOfLists:
        dicti = {}
        for elem in lista:
            try:
                result = re.search(':(.*)=', elem)
                poznatiFeature = result.group(1)
                result2 = re.search('=(.*)', elem)
                poznatiFeature_value = result2.group(1)
                dicti[poznatiFeature] = poznatiFeature_value
            except:
                dicti['odg'] = elem
        listOfDict.append(dicti)
    #print(listOfDict)

    #ispis [PREDICTIONS]:
    D, X, y, featureValues = getInputData(testSetPath)
    allInput = []
    for line in D:
        pomocni = {}
        for i in range(0, len(X)):
            pomocni[X[i]] = line[i][:-1]
        allInput.append(pomocni)

    predictions = []
    for line in allInput:
        for lista in listOfDict:
            shared_items = {k: line[k] for k in line if k in lista and line[k] == lista[k]}
            if len(shared_items) == len(lista)-1:
                predictions.append(lista['odg'])
    #print(predictions)
    print("[PREDICTIONS]: " + ' '.join(predictions))

else:
    # ispis [BRANCHES]:
    print("[BRANCHES]: ")
    listOfDict = []
    for lista in treeInList:
        i = 1

        pomocna = []
        pomocna2 = {}
        for j in range(0, len(lista)-1, 2):
            pomocna.append(str(i) + ':' + lista[j] + '=' + lista[j+1][:-1])
            pomocna2[lista[j]] = lista[j+1]
            i += 1
        pomocna.append(lista[-1])

        pomocna2['odg'] = lista[-1]
        listOfDict.append(pomocna2)
        print(' '.join(pomocna))
    #print(listOfDict)


    # ispis [PREDICTIONS]:
    D, X, y, featureValues = getInputData(testSetPath)
    allInput = []
    for line in D:
        pomocni = {}
        for i in range(0, len(X)):
            pomocni[X[i]] = line[i]
        allInput.append(pomocni)

    predictions = []
    for line in allInput:
        for lista in listOfDict:
            shared_items = {k: line[k] for k in line if k in lista and line[k] == lista[k]}
            if len(shared_items) == len(lista)-1:
                predictions.append(lista['odg'])

    if len(predictions) == 0:
        y.sort()
        for i in range(0, len(D)):
            predictions.append(y[0])    # ako tu znacajku jos nismo vidjeli predictaj abecedno prvi iz y

    print("[PREDICTIONS]: " + ' '.join(predictions))


# ispis [ACCURACY]:
correct = 0
total = len(D)
i = -1
for line in D:
    i += 1
    lineOdg = re.sub(r'[^a-zA-Z]', '', line[-1])
    try:
        if lineOdg == predictions[i]:
            correct += 1
    except:
        continue
print("[ACCURACY]: ", f'{correct/total:1.5f}')


# ispis [CONFUSION_MATRIX]:
rowColCount = len(set(y))
mat = [0] * rowColCount
for i in range(0, rowColCount):
    mat[i] = [0] * rowColCount          # [[0, 0], [0, 0]]
redosljed = list(set(y))
redosljed.sort()                        # ['False', 'True']
for i in range(0, len(y)):
    row = redosljed.index(y[i])
    col = redosljed.index(predictions[i])
    mat[row][col] += 1
print('[CONFUSION_MATRIX]:')
for elem in mat:
    string = ' '.join(str(e) for e in elem)
    print(string)
