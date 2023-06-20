from collections import deque
import heapq
import queue
from re import T, U

def getInputData(inputFile):
    with open(inputFile) as f:
        file = [line.rstrip('\n') for line in f]

    for element in file:
        if element.startswith('#'):
            file.remove(element)

    if len(file) == 0:
        return 'Unesen je krivi file'

    else:
        for i in range(0, len(file)):
            file[i] = file[i].lower()
        return file[0:len(file)-1], file[len(file)-1] # lista ulaznih klauzula + ciljna klauzula

def getCommands(inputFile):
    with open(inputFile) as f:
        file = [line.rstrip('\n') for line in f]

    for element in file:
        if element.startswith('#'):
            file.remove(element)

    if len(file) == 0:
        return 'Unesen je krivi file'

    else:
        for i in range(0, len(file)):
            file[i] = file[i].lower()
        return file



# ako imamo [[a,b], [a,b]] onda izbaci jednu [a,b]
def izbaciDuplice(listOfLists):
    reduciranaListaLista = []
    for lista in listOfLists:
        if lista not in reduciranaListaLista:
            reduciranaListaLista.append(lista)
    return reduciranaListaLista

# pretvori listu u listu lista --> split po ' v '
def pretvoriULL(lista):
    listOfLists = []
    for klauzula in lista:
        pomocna = []

        klauzula = klauzula.split(' v ')
        for elem in klauzula:
            # faktorizacija: (a v a) = a 
            if elem not in pomocna:
                pomocna.append(elem)
        
        listOfLists.append(pomocna)
    
    return listOfLists 

# izbaci duple elem i izbrisi sve kluzule koji imaju (a v ~a)
def reducirajListu(lista):
    reducirana = []
    for elem in lista:
        if elem not in reducirana:
            reducirana.append(elem)

    brisi = False
    for elem in reducirana:
        # strategija brisanja: brisi (a v ~a)

        if elem.startswith('~'):
            if (elem[1:]) in reducirana:
                brisi = True

    if brisi:
        return []

    return reducirana

# izbaci duple elem i izbrisi sve kluzule koje imaju (a v ~a), izbaci subsetove 
def reduciraj(listOfLists):
    nova = []
    for lista in listOfLists:
        pomocna = reducirajListu(lista)
        if len(pomocna) > 0:
            nova.append(pomocna)

    # strategija brisanja: imamo (a v b) i (a v b v c) --> brisi (a v b v c)
    zaIzbacit = []
    for i in range(0, len(nova)-1):
        for j in range(i+1, len(nova)):
            # A.issubset(B) --> true ako je A subset od B
            if set(nova[i]).issubset(set(nova[j])):
                zaIzbacit.append(nova[j])

            elif set(nova[j]).issubset(set(nova[i])):
                zaIzbacit.append(nova[i])

    pomocnaLista = []
    for elem in zaIzbacit:
        if elem not in pomocnaLista:
            pomocnaLista.append(elem)
    for elem in pomocnaLista:
        nova.remove(elem)

    return nova

# uzmi k1 iz ulazne U skupPotpre i k2 iz skupPotpre i vrati listu svih kombinacija ali td jedna ima npr a a druga ~a
def odaberiDvijeKlauzule(ulazneKlauzule, skupPotpore):
    listaParova = []

    for klauzula in ulazneKlauzule:
        for kl in skupPotpore:
            for element in klauzula:
                for elem in kl:
                    if "~" in element:
                        if element[1:] == elem:
                            par = []
                            par.append(klauzula)
                            par.append(kl)
                            listaParova.append(par)
                            break

                    elif "~" in elem:
                        if elem[1:] == element:
                            par = []
                            par.append(klauzula)
                            par.append(kl)
                            listaParova.append(par)
                            break


    for i in range(0, len(skupPotpore)-1):
        for j in range(i+1, len(skupPotpore)):
            for element in skupPotpore[i]:
                for elem in skupPotpore[j]:
                    if "~" in element:
                        if element[1:] == elem:
                            par = []
                            par.append(skupPotpore[i])
                            par.append(skupPotpore[j])
                            listaParova.append(par)
                            break

                    elif "~" in elem:
                        if elem[1:] == element:
                            par = []
                            par.append(skupPotpore[i])
                            par.append(skupPotpore[j])
                            listaParova.append(par)
                            break
           
    return listaParova
    
# razrijesi k1 i k2 i vrati roditelja 
def resolve(par):
    k1 = par[0]
    k2 = par[1]
    
    pomocnak1 = []
    for elem in k1:
        pomocnak1.append(elem)

    pomocnak2 = []
    for elem in k2:
        pomocnak2.append(elem)

    micik1 = []
    micik2 = []
    for znak in k1:
        for char in k2:
            if znak.startswith('~'):
                if char == znak[1:]:
                    micik1.append(znak)
                    micik2.append(char)
            else:
                if char == '~' + znak:
                    micik1.append(znak)
                    micik2.append(char)

    for elem in micik1:
        pomocnak1.remove(elem)
    for elem in micik2:
        pomocnak2.remove(elem)
    pomocnak1.extend(pomocnak2)

    pomocnak1 = reducirajListu(pomocnak1)

    if (len(pomocnak1) == 0):
        return('NIL')

    return pomocnak1


def REZOLUCIJA_OPOVRGAVANJEM(ulazneKlauzule, cilj):
    path = {}                                       # dict svih klauzula 
    brojac = 1
    for elem in ulazneKlauzule:
        pomocna = []
        pomocna.append(elem)
        pomocna.append('0')
        pomocna.append('0')
        path[brojac] = pomocna 
        brojac += 1
    ulazneKlauzule = pretvoriULL(ulazneKlauzule)      # list --> list of lists (radi faktorizaciju)
    ulazneKlauzule = izbaciDuplice(ulazneKlauzule)    # ono sto set radi sam mi moramo s fjom
    ulazneKlauzule = reduciraj(ulazneKlauzule)        # strategija brisanja x2

    lista = []                                                      # list
    lista.append(cilj)
    lista = pretvoriULL(lista)
    lista = reduciraj(lista)

    ciljnaKlauzula = []                                             # list of lists
    for elem in lista[0]:
        if elem.startswith('~'):
            ciljnaKlauzula.append(elem[1:])
        else:
            ciljnaKlauzula.append('~' + elem)
    ciljnaKlauzula = pretvoriULL(ciljnaKlauzula)
    ciljnaKlauzula = izbaciDuplice(ciljnaKlauzula)    
    ciljnaKlauzula = reduciraj(ciljnaKlauzula)  

    for elem in ciljnaKlauzula:
        pomocna = []
        pomocna.append(' v '.join(elem))
        pomocna.append(0)
        pomocna.append(0)
        path[brojac] = pomocna 
        brojac += 1

    brojOsnovnihKlauzula = brojac

    skupPotpore = []
    for ciljno in ciljnaKlauzula:
        skupPotpore.append(ciljno)
    skupPotpore = izbaciDuplice(skupPotpore)
    skupPotpore = reduciraj(skupPotpore)

    sveKlauzule = []
    for lista in ulazneKlauzule:
        sveKlauzule.append(lista)
    for elem in skupPotpore:
        sveKlauzule.append(elem)
    sveKlauzule = izbaciDuplice(sveKlauzule)
    sveKlauzule = reduciraj(sveKlauzule)

    gotovi = False

    while True:
        parovKlauzula = []
        parovKlauzula = odaberiDvijeKlauzule(ulazneKlauzule, skupPotpore)

        for par in parovKlauzula:
            roditelj = resolve(par)
            value1 = [min(str(k) for k,v in path.items() if v[0] == ' v '.join(par[0]))]
            value2 = [min(str(k) for k,v in path.items() if v[0] == ' v '.join(par[1]))]

            if roditelj == 'NIL':
                pomocna = []
                pomocna.append(roditelj)
                pomocna.append(value1[0])
                pomocna.append(value2[0])
                path[brojac] = pomocna 

                value1 = int(value1[0])
                value2 = int(value2[0])

                zaIspis = []    # lista rednih brojeva klauzula koje cemo ispisavt kao bitne 
                q = deque()     # red u koji spremamo redne brojeve od k1 i k2 za svakog rodtelja 

                zaIspis.append(brojac)
                if value1 != 0 and value1 > brojOsnovnihKlauzula:
                    zaIspis.append(value1)
                    q.append(value1)
                if value2 != 0 and value2 > brojOsnovnihKlauzula:
                    zaIspis.append(value2)
                    q.append(value2)

                gotovi = True
                while len(q) > 0:
                    elem = q.popleft()
                    if elem == 0:
                        continue
                    roditelj = path[elem]
                    value1 = int(roditelj[1])
                    value2 = int(roditelj[2])
                    if value1 != 0 and value1 > brojOsnovnihKlauzula:
                        zaIspis.append(value1)
                        q.append(value1)
                    if value2 != 0 and value2 > brojOsnovnihKlauzula:
                        zaIspis.append(value2)
                        q.append(value2)
                                     
                zaIspis.sort()
                #print('za ispis: ', zaIspis)

                # print osnovnih klauzula
                for i in range(1, brojOsnovnihKlauzula):
                    roditelj = path[i]
                    print(str(i) + ': ' + roditelj[0])
                print('===============')

                # print izvedenih klauzula 
                for elem in zaIspis:
                    roditelj = path[elem]
                    print(str(elem) + ': ' + roditelj[0] + ' (' + str(roditelj[1]) + ', ' + str(roditelj[2]) + ')')
                print('===============')
                
                print('[CONCLUSION]: ' + cilj + ' is true')
                gotovi = True
                break

            pomocna = []
            pomocna.append(' v '.join(roditelj))
            pomocna.append(value1[0])
            pomocna.append(value2[0])
            path[brojac] = pomocna 
            brojac += 1

            skupPotpore.append(roditelj)
            skupPotpore = izbaciDuplice(skupPotpore)
            skupPotpore = reduciraj(skupPotpore)

        if gotovi:
            break

        if all(item in sveKlauzule for item in skupPotpore):
            print('[CONCLUSION]: ' + cilj + ' is unknown')
            break
        
        for elem in skupPotpore:
            sveKlauzule.append(elem)
        #sveKlauzule = izbaciDuplice(sveKlauzule)
        sveKlauzule = reduciraj(sveKlauzule)

    return

def COOKING(ulazneKlauzule, cilj, popisNaredbi):
    sveKlauzuel = []
    for elem in ulazneKlauzule:
        sveKlauzuel.append(elem)
    sveKlauzuel.append(cilj)

    for naredba in popisNaredbi:
        privremeniCilj = str

        if naredba.endswith('?'):
            privremeniCilj = naredba[0:len(naredba)-2]
            print('Users command: ', naredba)
            REZOLUCIJA_OPOVRGAVANJEM(sveKlauzuel, privremeniCilj)
            print()
        elif naredba.endswith('+'):
            sveKlauzuel.append(naredba[0:len(naredba)-2])
            print('Users command: ', naredba)
            print('Added', naredba[0:len(naredba)-2])
            print()
        else:
            sveKlauzuel.remove(naredba[0:len(naredba)-2])
            print('Users command: ', naredba)
            print('Removed', naredba[0:len(naredba)-2])
            print()

    return 