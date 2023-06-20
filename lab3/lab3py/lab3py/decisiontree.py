import math
import re


class Node:
    def __init__(self):
        self.value = None       # weather
        self.next = None        # humidity
        self.children = None    # sunny, rainy, cloudly

# klasa koja gradi stablo odluke 
class DecisionTree:
    def __init__(self, D, X, y):
        self.D = D                          # cijeli skup ulaznih podataka bez 1.red (bez labela) = cijeli .csv file bez 1. red
        self.X = X                          # sva imena zancajki ['wather', 'wind', 'humidity', 'temperature']
        self.y = y                          # svi y: ['no', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'no']
        self.yCategories = list(set(y))     # samo unique y: ['no', 'yes']
        self.node = None

        D_indexes = [x for x in range(0, len(self.D))]  # [0,1,2,...13] = indexi ulaznih podataka 
        self.entropy = self.getEntropy(D_indexes)       # inicijalna entropija sustava i sve znacajke ju imaju istu 

    def getEntropy(self, D_indexes):  
        # odredi primjere koje gledmao za trenutnu znacajku   
        allLabels = [self.y[x] for x in D_indexes]  # uzmi samo one y-one za koje trenutno racunamo entropiju (indexi def u D_indexes)
        numOfLabelsInCategory = [allLabels.count(x) for x in self.yCategories]    # [9, 5] == {'da': 9, 'ne': 5}
        
        # izracunaj entropiju trenutne znacajke 
        entropy = 0
        for count in numOfLabelsInCategory:
            if count == 0:
                entropy = 0
            else:
                entropy += (-count / len(D_indexes)) * math.log2(count/len(D_indexes))
        return entropy

    def getIG(self, D_indexes, X_index):  
        # odredi sve value koje trenutni feature ima i njihov count 
        allFeatureValues = [self.D[x][X_index] for x in D_indexes]          # ['sunny', 'sunny', 'cloudy', 'rainy', 'rainy', 'rainy', 'cloudy', 'sunny', 'sunny', 'rainy', 'sunny', 'cloudy', 'cloudy', 'rainy']
        allUniqueFeatureValues = list(set(allFeatureValues))                # ['sunny', 'rainy', 'cloudy']
        allUniqueFeatureValuesCount = [allFeatureValues.count(x) for x in allUniqueFeatureValues]   # [5, 5, 4]

        # odredi listu ind pojavljivanja svakog valua za trenutni feature i spremi to u listu 
        allUniqueFeatureValuesIndexes = []
        for value in allUniqueFeatureValues:
            ind = []
            for i in range (0, len(allFeatureValues)):
                if allFeatureValues[i] == value:
                    ind.append(D_indexes[i])
            allUniqueFeatureValuesIndexes.append(ind)
        # print(allUniqueFeatureValuesIndexes)  [[2, 6, 11, 12], [0, 1, 7, 8, 10], [3, 4, 5, 9, 13]]
        #        na gornjim ind pojavljuju se:      cloudly           sunny             rainy

        nodeEntropy =  self.getEntropy(D_indexes)   # entropija trenutne znacajke 
        ig = nodeEntropy - sum([(val_count / len(D_indexes)) * self.getEntropy(val_id) 
                                for val_count, val_id in zip(allUniqueFeatureValuesCount, allUniqueFeatureValuesIndexes)])
        return ig  # ig = information gain za trenutni node (npr weather)

    def getMaxIG(self, D_indexes, X_indexes):
        # odredi max ig za trenuntno raspolozive feature (one koje jos nismo iskoristili)      #     ig(weather)             ig(temp)            ig(hum)             ig(wind)
        igForAllFeatures = [self.getIG(D_indexes, X_index) for X_index in X_indexes]           # [0.31365906539897026, 0.10416052657234964, 0.04606073001648636, 0.003558192623777545]
        indexOfMaxElem = X_indexes[igForAllFeatures.index(max(igForAllFeatures))]              # 0
        return indexOfMaxElem

    def ID3init(self):
        D_indexes = [x for x in range(0, len(self.D))]  # [0,1,2,...13]
        X_indexes = [x for x in range(0, len(self.X))]  # [0,1,2,3]
        self.node = self.ID3(D_indexes, X_indexes, self.node)

    def ID3(self, D_indexes, X_indexes, node):
        # ako je stablo prazno inicijaliziraj novi node (korijen)
        if not node:
            node = Node()
        
        labels = [self.y[x] for x in D_indexes]    # ['no', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'no']
        
        # ako svi primjeri iz D imaju istu vrijednost y, vrati node
        if len(set(labels)) == 1:
            node.value = self.y[D_indexes[0]]
            return node

        # ako smo dodali sve feature u stablo vrati klasu od y koja se najcesce pojavljuje 
        if len(X_indexes) == 0:
            node.value = max(set(labels), key=labels.count)
        
        else:
            # uzmi feature s max ig
            featureIdWithMaxIG = self.getMaxIG(D_indexes, X_indexes)    # 0
            featureNameWithMaxIG = self.X[featureIdWithMaxIG]           # X[0] = weather
            node.value = featureNameWithMaxIG                           # novi node je weather
            #print(featureNameWithMaxIG)

            # dodaj svu djecu od odabranog featura (npr svu djecu od weather)
            node.children = []
            children = list(set([self.D[x][featureIdWithMaxIG] for x in D_indexes]))    # ['cloudy', 'sunny', 'rainy']
            #print(children)

            # dodaj djecu u stablo 
            for child in children:
                newChild = Node()
                newChild.value = child          # cloudy
                node.children.append(newChild)
                #print(child)

                newChildIndexes = []            # [2, 6, 11, 12] --> indexi u D u kojima je weather=cloudly
                for index in D_indexes:
                    if self.D[index][featureIdWithMaxIG] == child:
                        newChildIndexes.append(index)

                #if len(newChildIndexes) > 0:
                    # zovi rekurzivno ID3 ali s novim D_indexes, X_indexes i node
                newD_indexes = newChildIndexes # vec smo izracunali gore 
                newX_indexes = [x for x in X_indexes if x != featureIdWithMaxIG]    # uzmi sve X_indexes osim trenutnog featura za kojeg dodajemo djecu i svih onih za koje smo to vec napravili 
                newChild.next = self.ID3(newD_indexes, newX_indexes, newChild.next) # newChild.next je feature koji ide nakon trenutnog featura (npr nakon weather ide humidity)

                #else:
                #    newChild.next = max(set(labels), key=labels.count)
        return node

    def getBranches(self, graph, currNode, prevNode):
        if currNode == prevNode:
            return [[currNode]]
        try:
            return[[currNode] + path for child in graph[currNode] for path in self.getBranches(graph, child, currNode)]
        except:
            return [[currNode]]

    def displayTreeInit(self):
        graph = self.displayTree(self.node, None, 1, {}) # dict kojima su key feature/velue od feature a value njihovi sljedbenici 

        for pairs in graph.items():
            if not isinstance(pairs[1], list):
                lista = []
                lista.append(pairs[1])
                graph[pairs[0]] = lista
        #print(graph)                                   # {'weather': ['rainy0', 'sunny0', 'cloudy0'], 'rainy0': ['wind'], 'wind': ['weak3', 'strong3'], ...}

        lol = self.getBranches(graph, list(graph.keys())[0], None) # vraca list of lists koji nam treba za ispis [BRANCHES]
        #print(lol)                                     # [['weather', 'rainy0', 'wind', 'strong3', 'no'], ['weather', 'rainy0', 'wind', 'weak3', 'yes'], ...]
        return lol

    def displayTree(self, currNode, prevNode, depth, graph):
        if currNode.value in self.yCategories:
                #print("\t"*depth, "[{0}]".format(currNode.value)) # ispis yes/no
                #print(depth)
                graph[prevNode] = currNode.value
        else:
                #print("\t"*depth, "{0}".format((currNode.value).upper())) # ispis WEATHER
                #print(depth)
                graph[currNode.value] = []

        depth += 1
        if currNode.children:
            for child in currNode.children:
                #print("\t"*depth, "{0}".format(child.value))       # ispis cloudy0 --> napravljeno da razlikujemo True i False za razlicite znacajke
                #print("\t"*depth, "{0}".format((child.value))[:-1]) # ispis cloudy
                #print(depth)
                graph[currNode.value].append(child.value)
                graph[child.value] = (child.next).value
                self.displayTree(child.next, child.value, depth+1, graph)
            depth += 1
    
        return graph





def getInputData(file):
    with open(file) as f:
        file = [line.rstrip('\n') for line in f]
    ###print(file)

    D = file[1:]

    D_listOfLists = []
    i = 0
    for line in D:
        linesplit = line.split(',')
        maxID = len(linesplit)

        novaLista = []
        for i in range(0, maxID):
            elem = linesplit[i]
            elem = elem + str(i)
            novaLista.append(elem)
        linesplit = novaLista
        D_listOfLists.append(linesplit)
    #print('--- D ---: ', D_listOfLists)
    ###print()

    prviRed = file[0].split(',')
    X = prviRed[:len(prviRed)-1]
    #print('--- X ---: ', X)
    ###print()

    y = []
    brojac = 0
    for line in file:
        brojac += 1
        if brojac == 1:
            continue
        lsplit = line.split(',')
        y.append(lsplit[-1])
    #y = list(dict.fromkeys(y))
    ##print('--- y ---: ', y)
    ###print()

    featureValues = {}
    for feature in X:
        featureValues[feature] = []

    for line in D:
        lineSplit = line.split(',')
        for i in range(0, len(lineSplit)-1):
            featureValues[X[i]].append(lineSplit[i])
            featureValues[X[i]] = list(dict.fromkeys(featureValues[X[i]]))
    ##print('--- featureValues ---: ', featureValues)
    ###print()

    return D_listOfLists, X, y, featureValues

def getPrediction(D, X, pomocna):
    dicti = {}
    for elem in pomocna:
        result = re.search(':(.*)=', elem)
        poznatiFeature = result.group(1)
        poznatiFeature_index = X.index(poznatiFeature)
        result2 = re.search('=(.*)', elem)
        poznatiFeature_value = result2.group(1)
        dicti[poznatiFeature_index] = poznatiFeature_value

    mogucePredikcije = []
    for line in D:
        brojac = 0
        for key in dicti.keys():
            if line[key][:-1] == dicti[key]:
                brojac += 1
        if brojac == len(dicti):
            mogucePredikcije.append(line[-1][:-1])
    mogucePredikcije.sort()
    
    dicti = {}
    for elem in mogucePredikcije:
        if elem not in dicti:
            dicti[elem] = 0
    
    for elem in mogucePredikcije:
        dicti[elem] += 1

    pred = max(dicti, key=dicti.get)  # vrati najvjerojatniju predikciju 
    return pred