from re import search
import heapq
from queue import PriorityQueue

def getInputData(inputFile):
    with open(inputFile) as f:
        file = [line.rstrip('\n') for line in f]

    for element in file:
        if element.startswith('#'):
            file.remove(element)

    ps_dict = {}
    if search(' ', file[0]):
        return 'Unesen je krivi file'

    else:
        # opisnik prostora stanja
        ps_dict['s0'] = file[0]
        ps_dict['goal'] = file[1]
        for i in range(2, len(file)):
            string_list = file[i].split(':')
            ps_dict[string_list[0]] = string_list[1]
        return ps_dict;
         
def getInputDataHeuristic(inputFile):
    with open(inputFile) as f:
        file = [line.rstrip('\n') for line in f]

    for element in file:
        if element.startswith('#'):
            file.remove(element)

    hf_dict = {}
    if search(' ', file[0]):
         # opisnik hauristicke fje
        for element in file:
            string_list = element.split(':')
            hf_dict[string_list[0]] =  string_list[1]
        return hf_dict; # dictionary 

    else:
        return 'Unesen je krivi file'


def BFS(ulazniPodatci):
    s0 = ulazniPodatci['s0']
    goal = ulazniPodatci['goal']
    goal = goal.split(' ')
    listaPrijelaza = dict(list(ulazniPodatci.items())[2:]) # bez s0 i goal 

    o = []              # lista open (lista se ponasa kao red)
    visited = set()     # nema ponavljanja elemenata
    states_visited = 0  # za ispis

    o.append(s0)

    # potrebno za pronalazak puta 
    roditelj = dict()   
    roditelj[s0] = None

    # o, roditelj, path spremaju na nacin: ['Pula,20', 'Motovun,13']
    # visited sprema na nacin:             ['Pula', 'Motovun']


    while (len(o) > 0):
        n = o.pop(0)
        n = n.split(',')

        visited.add(n[0])
        states_visited += 1

        if (n[0] in goal):
            path_length = 0
            total_cost = 0
            path = []
            pathSamoStanja = []

            trenutni = ','.join(n)
            path.append(trenutni)

            while roditelj[trenutni] is not None:
                path.append(roditelj[trenutni])
                trenutni = roditelj[trenutni]
                
            path.reverse()

            # racunanje total_costa, path_lengtha i patha za ispis
            for element in path:
                element = element.split(',')
                pathSamoStanja.append(element[0])
                try:
                    total_cost += float(element[1])
                except:
                    pass
                path_length += 1

            pathZaIspis = ' => '.join([str(stanje) for stanje in pathSamoStanja])

            print('# BFS')
            print('[FOUND_SOLUTION]: ', 'yes')
            print('[STATES_VISITED]: ', states_visited)
            print('[PATH_LENGTH]: ', path_length)
            print('[TOTAL_COST]: ', total_cost)
            print('[PATH]: ', pathZaIspis)
            return
        
        djeca = listaPrijelaza[n[0]]
        djeca = djeca.split(' ')

        # djeca: ['', 'fail_lab,1', 'complete_lab,4'] - moramo maknut ''
        if (djeca[0] == ''):
            djeca.pop(0)
        
        heapq.heapify(djeca) # slozit djecu abecedno 

        for dijete in djeca:   
            dijete = dijete.split(',')    # zbog visited
            if dijete[0] not in visited:
                visited.add(dijete[0]) 
                o.append(','.join(dijete)) 
                roditelj[','.join(dijete)] = ','.join(n)
                
def UCS(ulazniPodatci):
    s0 = ulazniPodatci['s0']
    goal = ulazniPodatci['goal']
    goal = goal.split(' ')
    listaPrijelaza = dict(list(ulazniPodatci.items())[2:]) # bez s0 i goal 

    o = PriorityQueue()  # prioritetni red open koji prima tuplove
    visited = set()      # nema ponavljanja elemenata
    states_visited = 0   # za ispis

    s0_tuple = tuple(map(str, s0.split(',')))  # prebacivanje u tuple da dobijemo cijenu kao int --> s0_tuple = ('enroll_artificial_intelligence')
    s0_tuple_copy = (0, s0_tuple[0])          # s0_tuple_copy = (0, 'enroll_artificial_intelligence')
    o.put(s0_tuple_copy)

    # potrebno za pronalazak puta 
    roditelj = dict() 
    roditelj[s0_tuple_copy] = None     # pocetni clan nema roditelja 

    while (not o.empty()):
        n = o.get()

        # ako smo dosli do goal state-a
        if (n[1] in goal):
            path_length = 0
            total_cost = 0
            path = []
            pathSamoStanja = []

            trenutni = n
            path.append(trenutni)

            while roditelj[trenutni] is not None:
                path.append(roditelj[trenutni])
                trenutni = roditelj[trenutni]

            path.reverse()

            # racunanje total_costa, path_lengtha i patha za ispis
            for element in path:
                pathSamoStanja.append(element[1])
                path_length += 1

            zadnji = path[-1]
            total_cost = float(zadnji[0])

            pathZaIspis = ' => '.join([str(stanje) for stanje in pathSamoStanja])
           
            print('# UCS')
            print('[FOUND_SOLUTION]: ', 'yes')
            print('[STATES_VISITED]: ', states_visited)
            print('[PATH_LENGTH]: ', path_length)
            print('[TOTAL_COST]: ', total_cost)
            print('[PATH]: ', pathZaIspis)
            return
        
        visited.add(n[1])
        states_visited += 1

        djeca = listaPrijelaza[n[1]]
        djeca = djeca.split(' ')

        # djeca: ['', 'fail_lab,1', 'complete_lab,4'] - moramo maknut ''
        if (djeca[0] == ''):
            djeca.pop(0)
        
        #heapq.heapify(djeca) # slozit djecu abecedno 

        for dijete in djeca:   
            # svako dijete prebaci u tuple oblika (cijena, naziv)
            dijete_tuple = tuple(map(str, dijete.split(',')))
            dijete_tuple_copy = (int(dijete_tuple[1]), dijete_tuple[0])

            # pregledavaj samo neobidena stanja 
            if dijete_tuple_copy[1] not in visited:
                pathCost = n[0] + dijete_tuple_copy[0]  # cijena od pocetnog go trenutnog 
                
                oLowerCost = False      # provjera je li u open vec stanje ovo dijete koje ima manju cijenu od trenutno izracunate  
                temp = list(o.queue)    # kopiraj prioritetni red u listu td mozemo mica elemente 
                
                for elem in temp:
                    # trazimo samo stanje u o redu koje je jednako trenutnom stanju tj djetetu  
                    if (not elem[1] == dijete_tuple_copy[1]):
                        continue

                    # u o je stavrno dijete kao i nase, samo s manjom cijenom --> ne dodajemo nase dijete 
                    if (elem[0] <= pathCost):
                        oLowerCost = True

                    # u o je isto dijete samo s vecom cijenom --> makni ga i kasnije dodaj nase novo dijete (tj isto dijete al nova cijena)
                    else:
                        temp.remove(elem)

                    break
                
                # ipak je nase dijete 'jeftinije' od onog sta je bilo u o 
                if (not oLowerCost):
                    # promijeni cijenu djeteta -- ovako zato sto je tuple unchangeable 
                    tempList = list(dijete_tuple_copy)
                    tempList[0] = pathCost
                    dijete_tuple_copy = tuple(tempList)

                    # dodajemo dijete u o i pamtimo mu rodtelja 
                    # o je prioritetni red pa sam slaze po cijenama jer su tuplovi u njemu (cijena, naziv)
                    o.put(dijete_tuple_copy) 
                    roditelj[dijete_tuple_copy] = n

def A_STAR(ulazniPodatci, ulazniPodatciHeuristika, fileHeur):
    s0 = ulazniPodatci['s0']
    goal = ulazniPodatci['goal']
    goal = goal.split(' ')
    listaPrijelaza = dict(list(ulazniPodatci.items())[2:]) # bez s0 i goal 
    listaHeuristika = dict(list(ulazniPodatciHeuristika.items()))

    o = PriorityQueue()  # prioritetni red open koji prima tuplove
    visited = set()      # nema ponavljanja elemenata
    states_visited = 0   # za ispis

    s0_tuple = tuple(map(str, s0.split(',')))  # prebacivanje u tuple da dobijemo cijenu kao int --> s0_tuple = ('enroll_artificial_intelligence')
    s0_tuple_copy = (0, s0_tuple[0])          # s0_tuple_copy = (0, 'enroll_artificial_intelligence')
    
    # dodajemo f = cijena + heuristika kao 3. elem s0_tuple_cop
    tempList = list(s0_tuple_copy)
    tempList.append(int(listaHeuristika[s0_tuple_copy[1]]))
    tempList.insert(0, tempList[0] + tempList[2])
    s0_tuple_copy = tuple(tempList)
    
    o.put(s0_tuple_copy)

    # potrebno za pronalazak puta 
    roditelj = dict() 
    roditelj[s0_tuple_copy] = None     # pocetni clan nema roditelja 

    while (not o.empty()):
        n = o.get()

        # ako smo dosli do goal state-a
        if (n[2] in goal):
            path_length = 0
            total_cost = 0
            path = []
            pathSamoStanja = []

            trenutni = n
            path.append(trenutni)

            while roditelj[trenutni] is not None:
                path.append(roditelj[trenutni])
                trenutni = roditelj[trenutni]

            path.reverse()

            # racunanje total_costa, path_lengtha i patha za ispis
            for element in path:
                pathSamoStanja.append(element[2])
                path_length += 1

            zadnji = path[-1]
            total_cost = float(zadnji[1])

            pathZaIspis = ' => '.join([str(stanje) for stanje in pathSamoStanja])
           
            print('# A-STAR ' + fileHeur)
            print('[FOUND_SOLUTION]: ', 'yes')
            print('[STATES_VISITED]: ', states_visited)
            print('[PATH_LENGTH]: ', path_length)
            print('[TOTAL_COST]: ', total_cost)
            print('[PATH]: ', pathZaIspis)
            return
        
        visited.add(n[2])
        states_visited += 1

        djeca = listaPrijelaza[n[2]]
        djeca = djeca.split(' ')

        # djeca: ['', 'fail_lab,1', 'complete_lab,4'] - moramo maknut ''
        if (djeca[0] == ''):
            djeca.pop(0)
        
        #heapq.heapify(djeca) # slozit djecu abecedno 

        for dijete in djeca:   
            # svako dijete prebaci u tuple oblika (cijena, naziv)
            dijete_tuple = tuple(map(str, dijete.split(',')))
            dijete_tuple_copy = (int(dijete_tuple[1]), dijete_tuple[0])
            tempList = list(dijete_tuple_copy)
            tempList.append(int(listaHeuristika[dijete_tuple_copy[1]]))
            tempList.insert(0, tempList[0] + tempList[2])
            dijete_tuple_copy = tuple(tempList)

            # pregledavaj samo neobidena stanja 
            if dijete_tuple_copy[2] not in visited:
                pathCost = n[1] + dijete_tuple_copy[1]  # cijena od pocetnog go trenutnog 
                totalCost = pathCost + dijete_tuple_copy[3] # cijena od pocetnog go trenutnog + heuristika trenutnog
                
                oLowerCost = False      # provjera je li u open vec stanje ovo dijete koje ima manju cijenu od trenutno izracunate  
                temp = list(o.queue)    # kopiraj prioritetni red u listu td mozemo mica elemente 
                
                for elem in temp:
                    # trazimo samo stanje u o redu koje je jednako trenutnom stanju tj djetetu  
                    if (not elem[2] == dijete_tuple_copy[2]):
                        continue

                    # u o je stavrno dijete kao i nase, samo s manjom cijenom --> ne dodajemo nase dijete 
                    if (elem[0] <= totalCost):
                        oLowerCost = True

                    # u o je isto dijete samo s vecom cijenom --> makni ga i kasnije dodaj nase novo dijete (tj isto dijete al nova cijena)
                    else:
                        temp.remove(elem)

                    break
                
                # ipak je nase dijete 'jeftinije' od onog sta je bilo u o 
                if (not oLowerCost):
                    # promijeni cijenu djeteta -- ovako zato sto je tuple unchangeable 
                    tempList = list(dijete_tuple_copy)
                    tempList[0] = totalCost
                    tempList[1] = pathCost
                    dijete_tuple_copy = tuple(tempList)

                    # dodajemo dijete u o i pamtimo mu rodtelja 
                    # o je prioritetni red pa sam slaze po cijenama jer su tuplovi u njemu (cijena, naziv)
                    o.put(dijete_tuple_copy) 
                    roditelj[dijete_tuple_copy] = n


def UCS2(s0, listaPrijelaza, goal):
    o = PriorityQueue()  # prioritetni red open koji prima tuplove
    visited = set()      # nema ponavljanja elemenata

    s0_tuple = tuple(map(str, s0.split(',')))  # prebacivanje u tuple da dobijemo cijenu kao int --> s0_tuple = ('enroll_artificial_intelligence')
    s0_tuple_copy = (0, s0_tuple[0])          # s0_tuple_copy = (0, 'enroll_artificial_intelligence')
    o.put(s0_tuple_copy)

    # potrebno za pronalazak puta 
    roditelj = dict() 
    roditelj[s0_tuple_copy] = None     # pocetni clan nema roditelja 

    while (not o.empty()):
        n = o.get()

        # ako smo dosli do goal state-a
        if (n[1] in goal):
            total_cost = 0
            path = []

            trenutni = n
            path.append(trenutni)

            while roditelj[trenutni] is not None:
                path.append(roditelj[trenutni])
                trenutni = roditelj[trenutni]

            path.reverse()

            zadnji = path[-1]
            total_cost = float(zadnji[0])

            return total_cost
        
        visited.add(n[1])

        djeca = listaPrijelaza[n[1]]
        djeca = djeca.split(' ')

        # djeca: ['', 'fail_lab,1', 'complete_lab,4'] - moramo maknut ''
        if (djeca[0] == ''):
            djeca.pop(0)
        
        #heapq.heapify(djeca) # slozit djecu abecedno 

        for dijete in djeca:   
            # svako dijete prebaci u tuple oblika (cijena, naziv)
            dijete_tuple = tuple(map(str, dijete.split(',')))
            dijete_tuple_copy = (int(dijete_tuple[1]), dijete_tuple[0])

            # pregledavaj samo neobidena stanja 
            if dijete_tuple_copy[1] not in visited:
                pathCost = n[0] + dijete_tuple_copy[0]  # cijena od pocetnog go trenutnog 
                
                oLowerCost = False      # provjera je li u open vec stanje ovo dijete koje ima manju cijenu od trenutno izracunate  
                temp = list(o.queue)    # kopiraj prioritetni red u listu td mozemo mica elemente 
                
                for elem in temp:
                    # trazimo samo stanje u o redu koje je jednako trenutnom stanju tj djetetu  
                    if (not elem[1] == dijete_tuple_copy[1]):
                        continue

                    # u o je stavrno dijete kao i nase, samo s manjom cijenom --> ne dodajemo nase dijete 
                    if (elem[0] <= pathCost):
                        oLowerCost = True

                    # u o je isto dijete samo s vecom cijenom --> makni ga i kasnije dodaj nase novo dijete (tj isto dijete al nova cijena)
                    else:
                        temp.remove(elem)

                    break
                
                # ipak je nase dijete 'jeftinije' od onog sta je bilo u o 
                if (not oLowerCost):
                    # promijeni cijenu djeteta -- ovako zato sto je tuple unchangeable 
                    tempList = list(dijete_tuple_copy)
                    tempList[0] = pathCost
                    dijete_tuple_copy = tuple(tempList)

                    # dodajemo dijete u o i pamtimo mu rodtelja 
                    # o je prioritetni red pa sam slaze po cijenama jer su tuplovi u njemu (cijena, naziv)
                    o.put(dijete_tuple_copy) 
                    roditelj[dijete_tuple_copy] = n

def HEURISTIC_OPTIMISTIC(ulazniPodatci, ulazniPodatciHeuristika, fileHeur):
    print('# HEURISTIC_OPTIMISTIC ' + fileHeur)

    s0 = ulazniPodatci['s0']
    goal = ulazniPodatci['goal']
    goal = goal.split(' ')
    listaPrijelaza = dict(list(ulazniPodatci.items())[2:]) # bez s0 i goal 
    listaHeuristika = dict(list(ulazniPodatciHeuristika.items()))

    jeOptGlob = True
    for stanje in listaPrijelaza:
        jeOptLok = True
        stanjeHeur = float(listaHeuristika[stanje])
        pathCost = UCS2(stanje, listaPrijelaza, goal)

        if (stanjeHeur > pathCost):
            jeOptLok = False
            jeOptGlob = False

        if (jeOptLok):
            print('[CONDITION]: [OK] h(' + stanje + ') <= h*: ' + str(stanjeHeur) + ' <= ' + str(pathCost))
        else:
            print('[CONDITION]: [ERR] h(' + stanje + ') <= h*: ' + str(stanjeHeur) + ' <= ' + str(pathCost))
    
    if (jeOptGlob):
            print('[CONCLUSION]: Heuristic is optimistic.')
    else:
            print('[CONCLUSION]: Heuristic is not optimistic.')

def HEURISTIC_CONSISTENT(ulazniPodatci, ulazniPodatciHeuristika, fileHeur):
    print('# HEURISTIC_CONSISTENT ' + fileHeur)

    s0 = ulazniPodatci['s0']
    goal = ulazniPodatci['goal']
    goal = goal.split(' ')
    listaPrijelaza = dict(list(ulazniPodatci.items())[2:]) # bez s0 i goal 
    listaHeuristika = dict(list(ulazniPodatciHeuristika.items()))

    jeConGlob = True
    for stanje in listaPrijelaza:
        stanjeHeur = float(listaHeuristika[stanje])

        djeca = listaPrijelaza[stanje]
        djeca = djeca.split(' ')

        # djeca: ['', 'fail_lab,1', 'complete_lab,4'] - moramo maknut ''
        if (djeca[0] == ''):
            djeca.pop(0)

        for dijete in djeca:   
            jeConLok = True

            # svako dijete prebaci u tuple oblika (cijena, naziv)
            dijete_tuple = tuple(map(str, dijete.split(',')))
            dijete_tuple_copy = (int(dijete_tuple[1]), dijete_tuple[0])

            dijeteHeur = float(listaHeuristika[dijete_tuple_copy[1]])
            prijelazCost = float(dijete_tuple_copy[0])

            if (stanjeHeur > dijeteHeur + prijelazCost):
                jeConGlob = False
                jeConLok = False

            if (jeConLok):
                print('[CONDITION]: [OK] h(' + stanje + ') <= h(' + dijete_tuple_copy[1] + ') + c: ' + str(stanjeHeur) + ' <= ' +  str(dijeteHeur) + ' + ' + str(prijelazCost))
            else:
                print('[CONDITION]: [ERR] h(' + stanje + ') <= h(' + dijete_tuple_copy[1] + ') + c: ' + str(stanjeHeur) + ' <= ' +  str(dijeteHeur) + ' + ' + str(prijelazCost))

    if (jeConGlob):
        print('[CONCLUSION]: Heuristic is consistent.')
    else:
        print('[CONCLUSION]: Heuristic is not consistent.')

