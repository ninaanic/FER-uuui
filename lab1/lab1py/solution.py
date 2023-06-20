from functions import getInputData, getInputDataHeuristic, BFS, UCS, A_STAR, HEURISTIC_OPTIMISTIC, HEURISTIC_CONSISTENT
import argparse, os

parser = argparse.ArgumentParser()
parser.add_argument('--alg', help='Kratica za algoritam za pretrazivanje (vrijednosti: bfs, ucs, ili astar)', type=str, default="")
parser.add_argument('--ss', help='Putanja do opisnika prostora stanja', type=str, default="")
parser.add_argument('--h', help='Putanja do opisnika heuristike', type=str, default="")
parser.add_argument('--check-optimistic', help='Zastavica koja signalizira da se za danu heuristiku zeli provjeriti optimisticnost', default="", action='store_true')
parser.add_argument('--check-consistent', help='Zastavica koja signalizira da se za danu heuristiku zeli provjeriti konsistentnost', default="", action='store_true')
args = parser.parse_args()

#currentDir = os.getcwd()

ulazniPodatciPath = os.path.dirname(os.path.abspath(args.ss))
ulazniPodatci = getInputData(ulazniPodatciPath + '/' + args.ss)

if (args.h):
    ulazniPodatciHeuristikaPath = os.path.dirname(os.path.abspath(args.h))
    ulazniPodatciHeuristika = getInputDataHeuristic(ulazniPodatciHeuristikaPath + '/' + args.h)



if (args.alg == 'bfs'): 
    BFS(ulazniPodatci)
elif (args.alg == 'ucs'):
    UCS(ulazniPodatci)
else:
    A_STAR(ulazniPodatci, ulazniPodatciHeuristika, args.h)

if (args.check_optimistic):
    HEURISTIC_OPTIMISTIC(ulazniPodatci, ulazniPodatciHeuristika, args.h)

elif (args.check_consistent):
    HEURISTIC_CONSISTENT(ulazniPodatci, ulazniPodatciHeuristika, args.h)

