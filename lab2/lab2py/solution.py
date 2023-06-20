import sys, os
import time
from functions import getInputData, getCommands, REZOLUCIJA_OPOVRGAVANJEM, COOKING

args = sys.argv

if (args[1] == 'resolution'):
    start = time.time()

    #ulazniPodatciPath = '/Users/ninaanic/Tehnicke/6_semestar/UUUI/autograder/data/lab2/files'
    ulazniPodatciPath = os.path.dirname(os.path.abspath(args[2]))                              # path za autograder, zakomentirat ovaj gore 
    ulazneKlauzule, cilj = getInputData(ulazniPodatciPath + '/' + args[2]) 

    REZOLUCIJA_OPOVRGAVANJEM(ulazneKlauzule, cilj)
    end = time.time()
    print(f"Total time (seconds): {end - start}")

elif(args[1] == 'cooking'):
    start = time.time()
    #ulazniPodatciPath = '/Users/ninaanic/Tehnicke/6_semestar/UUUI/autograder/data/lab2/files'
    ulazniPodatciPath = os.path.dirname(os.path.abspath(args[2]))                               # path za autograder, zakomentirat ovaj gore 
    ulazneKlauzule, cilj = getInputData(ulazniPodatciPath + '/' + args[2]) 

    ulazniPodatciPath = os.path.dirname(os.path.abspath(args[3]))                               # path za autograder, zakomentirat ovaj gore 
    popisNaredbi = getCommands(ulazniPodatciPath + '/' + args[3])

    COOKING(ulazneKlauzule, cilj, popisNaredbi)
    end = time.time()
    print(f"Total time (seconds): {end - start}")

else:
    print('Unesen je krivi argument.')



# pokretanje lokalno:
# u folderu lab2py napista: /Users/ninaanic/.virtualenvs/srs/bin/python /Users/ninaanic/Tehnicke/6_semestar/UUUI/labosi/lab2/lab2py/solution.py cooking cooking_coffee.txt cooking_coffee_input.txt
#                      ili: /Users/ninaanic/.virtualenvs/srs/bin/python /Users/ninaanic/Tehnicke/6_semestar/UUUI/labosi/lab2/lab2py/solution.py resolution new_example_6.txt