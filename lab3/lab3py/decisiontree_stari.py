import math

class Node:
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__children = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def children(self):
        return self.__children

    def add_child(self, identifier):
        ##print('idennnnnn', identifier)
        self.__children.append(identifier)

(_ROOT, _DEPTH, _BREADTH) = range(3)
class Tree:

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, identifier, parent=None):
        node = Node(identifier)
        self[identifier] = node

        if parent is not None:
            self[parent].add_child(identifier)
        return node

    def display(self, identifier, depth=_ROOT):
        children = self[identifier].children
        if depth == _ROOT:
            print("{0}".format(identifier))
        else:
            print("\t"*depth, "{0}".format(identifier))

        depth += 1
        for child in children:
            if child != identifier:
                self.display(child, depth)  # recursive call
            else:
                print("\t"*depth, "{0}".format(child))
                depth += 1

    
    def getBranches(self, identifier, finalTree):
        if len(self[identifier].children) == 0:
            return [[identifier]]
        return[
            [identifier] + path for child in self[identifier].children for path in finalTree.getBranches(child, finalTree)
        ]
        
    def traverse(self, identifier, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from 
        # 'Essential LISP' by John R. Anderson, Albert T. Corbett, 
        # and Brian J. Reiser, page 239-241
        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            if mode == _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _BREADTH:
                queue = queue[1:] + expansion  # width-first

    def getPredictions(self, identifier, lineSplit, X, zaIspis, depth=_ROOT):
        children = self[identifier].children
        zaIspis.append(identifier)             
        depth += 1
        for child in children:
            if child in X:
                self.getPredictions(child, lineSplit, X, zaIspis, depth)  
            if child in lineSplit:
                self.getPredictions(child, lineSplit, X, zaIspis, depth)  
        return zaIspis

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item


def getInputData(file):
    with open(file) as f:
        file = [line.rstrip('\n') for line in f]
    ##print(file)

    D = file[1:]
    ##print('--- D ---: ', D)
    ##print()

    prviRed = file[0].split(',')
    X = prviRed[:len(prviRed)-1]
    ##print('--- X ---: ', X)
    ##print()

    y = []
    brojac = 0
    for line in file:
        brojac += 1
        if brojac == 1:
            continue
        lsplit = line.split(',')
        y.append(lsplit[-1])
    y = list(dict.fromkeys(y))
    ##print('--- y ---: ', y)
    ##print()

    featureValues = {}
    for feature in X:
        featureValues[feature] = []

    for line in D:
        lineSplit = line.split(',')
        for i in range(0, len(lineSplit)-1):
            featureValues[X[i]].append(lineSplit[i])
            featureValues[X[i]] = list(dict.fromkeys(featureValues[X[i]]))
    ##print('--- featureValues ---: ', featureValues)
    ##print()

    return D, X, y, featureValues

def ID3(D, X, y, featureValues, parentNode, tree, root, elemEntropy):
    #print('** parent', parentNode)
    yNums = {}                                  # y = {'no', 'yes'}; yNums = {'no': 5, 'yes': 9}
    for elem in y:
        yNums[elem] = 0

    for line in D:
        lineSplit = line.split(',')
        yNums[lineSplit[-1]] += 1
    ##print(yNums)

    # svaki korijen ima istu E pa ju mozemo racunat samo 1 
    E_feature = 0
    if elemEntropy == None:
        for elem in yNums:
            if yNums[elem] == 0:
                E_feature = 0
                break
            E_feature -= (yNums[elem]/len(D)) * math.log2(yNums[elem]/len(D))
        #print('E_feature', E_feature)
    else:
        E_feature = elemEntropy
        #print('E_feature', E_feature)

    IGlist = []
    i = 0
    for feature in X:
        #print('feature', feature)

        E_valuesList = []
        for value in featureValues[feature]:
            yNums = {}                                 
            for elem in y:
                yNums[elem] = 0
            #print(value)

            ukupno = 0
            for line in D:
                lineSplit = line.split(',')
                if lineSplit[i] == value:
                    yNums[lineSplit[-1]] += 1
                    ukupno += 1
            #print(yNums)
            ##print(ukupno)

            # izarcunaj E(feature, value)
            E_fatureValue = 0
            for elem in yNums:
                if yNums[elem] == 0:
                    E_fatureValue = 0
                    break
                E_fatureValue -= (yNums[elem]/ukupno) * math.log2(yNums[elem]/ukupno)
            #print(E_fatureValue)

            E_valuesList.append((ukupno/len(D)) * E_fatureValue)
        
        #print(E_valuesList)
        
        # izracunaj IG(D, feature) i spremi to u IGlist
        ig_values = 0
        for elem in E_valuesList:
            ig_values += elem
        IGlist.append(E_feature-ig_values)
        ##print(IGlist)
        i += 1

    #print('ig lista', IGlist)

    if len(IGlist) == 0:
        return tree, root

    maxElemIndex = -1 
    listaIndexa = []
    for i in range(0, len(IGlist)):
        if IGlist[i] == max(IGlist):
            listaIndexa.append(i)
    ##print('lista', listaIndexa)

    sortiranaLista = []
    if len(listaIndexa) > 1:
        for i in listaIndexa:
            sortiranaLista.append(X[i])
        sortiranaLista.sort()
        ##print(sortiranaLista)
        
        for i in range(0, len(X)):
            if X[i] == sortiranaLista[0]:
                maxElemIndex = i
                break

    else:
        maxElemIndex = listaIndexa[0]

    try:
        nextRoot = X[maxElemIndex]
    except:
        return
    #print('next root: ', nextRoot)
    ##print(maxElemIndex)

    gotovi = {}
    ##print('featureValues[nextRoot]', featureValues[nextRoot])
    for value in featureValues[nextRoot]:
        yNums = {}                                 
        for elem in y:
            yNums[elem] = 0

        ukupno = 0
        for line in D:
            lineSplit = line.split(',')
            ##print(lineSplit)
            if lineSplit[maxElemIndex] == value:
                yNums[lineSplit[-1]] += 1
                ukupno += 1

        ##print('val', value)
        ##print(yNums)
        zaDodat = []
        elemSNulom = []
        for elem in yNums:
            if yNums[elem] == 0:
                zaDodat.append(value)
                elemSNulom.append(elem)

        ##print('el s nulom', elemSNulom)
        ##print('za dodat 1dio', zaDodat)

        if len(zaDodat) > 0:
            zaDodat = list(dict.fromkeys(zaDodat))
            for elem in yNums:
                if elem not in elemSNulom:
                    zaDodat.append(elem)

            ##print('za dodat', zaDodat)
        
        if zaDodat != []:
            gotovi[zaDodat[0]] = zaDodat[1]
    #print(gotovi)

    if parentNode == None:
        tree = Tree()
        tree.add_node(nextRoot)
        for elem in featureValues[nextRoot]:
            ##print('elem', elem)
            tree.add_node(elem, nextRoot)
            if elem in gotovi:
                tree.add_node(gotovi[elem], elem)
        root = nextRoot

    else:
        ##print('next root', nextRoot)
        ##print('parent', parentNode)
        tree.add_node(nextRoot, parentNode)
        #tree.display(root)
        for elem in featureValues[nextRoot]:
            ##print('elem', elem)
            tree.add_node(elem, nextRoot)
            if elem in gotovi:
                tree.add_node(gotovi[elem], elem)
            
                
        #tree.display(root)

    #print('+++++++ Trnutno stablo: ')
    #tree.display(root)

    ##print()

    # izracunaj entrpiju
    for elem in featureValues[nextRoot]:
        if elem not in gotovi:
            #print(elem)
            # izracunaj entrpiju
            yNums = {}                                 
            for el in y:
                yNums[el] = 0

            ukupno = 0
            for line in D:
                lineSplit = line.split(',')
                if lineSplit[maxElemIndex] == elem:
                    yNums[lineSplit[-1]] += 1
                    ukupno += 1
            #print('yNums 123', yNums)

            # izarcunaj E(feature, value)
            E_fatureValue = 0
            for el in yNums:
                if yNums[el] == 0:
                    E_fatureValue = 0
                    break
                E_fatureValue -= (yNums[el]/ukupno) * math.log2(yNums[el]/ukupno)
            #print(E_fatureValue)
            
            #print(elem)
            noviD = []
            for line in D:
                lineSplit = line.split(',')
                if elem in lineSplit:
                    noviD.append(','.join(lineSplit[1:]))
            ##print(noviD)
            
            noviX = []
            for x in X:
                if x == nextRoot:
                    continue
                noviX.append(x)
            ##print(noviX)

            novifeatureValues = {}
            for x in noviX:
                novifeatureValues[x] = []
            for line in noviD:
                lineSplit = line.split(',')
                for i in range(0, len(lineSplit)-1):
                    novifeatureValues[noviX[i]].append(lineSplit[i])
                    novifeatureValues[noviX[i]] = list(dict.fromkeys(novifeatureValues[noviX[i]]))
            ##print(novifeatureValues)

            ID3(noviD, noviX, y, novifeatureValues, elem, tree, root, E_fatureValue)
            ##print('+++++++ Trnutno stablo: ')
            #tree.display(root)

    #tree.display(root)
    return tree, root

