### IMPORTS ###
import os
import sys
import random
import math
import argparse
import subprocess

from parser import parseFile
from evaluationTool import evaluateCode
from neighborhoodFunction import createNeighborhood, mutateRefactor
from refactorTool import seeRefactor,applyRefactor,copyRefactor,extractFileFeatures
from priorizationTool import prioritizeRefactors

### VARS ###

# Variable que contiene la direccion de todos los archivos temporales generados junto con su calidad.
codeEval = []

### FUNCTIONS ###

# Funcion recursiva que crea el menu principal para las refactorizaciones manuales.
def menu():    
    userApply = input("Do you want to apply this refactor? (y/n)")
    if userApply == 'y':
        return True
    elif userApply == 'n': 
        return False
    else:
        print("Invalid char. Try again.")
        menu()

#Funcion que devuelve el nombre del archivo de mejor calidad.
def getBestQuality(codeEval):
    maxTuple = min(codeEval, key=lambda item: item['quality'])
    return maxTuple['file']

# Inicia la refactorizacion manual.
def initManualRefactoring(haskellFile):
    refactors = prioritizeRefactors(parseFile(haskellFile),True)
    codeEval.append({"file": haskellFile,"quality": evaluateCode(refactors)})    
    
    listOfNeighbours = createNeighborhood(refactors,1)
    i = 0
    for neighbour in listOfNeighbours:
        for refactor in neighbour:
            if seeRefactor(haskellFile,refactor):
                continue
            if menu() == True:
                newFile = copyRefactor(haskellFile,str(i))
                initManualRefactoring(newFile)
                break

        i = i + 1

# Inicia la refactorizacion al azar.
def initRandomRefactoring(haskellFile,maxIterations):
    i = 0

    while True:    
        refactors = prioritizeRefactors(parseFile(haskellFile),False)
        codeEval.append({"file": haskellFile,"quality": evaluateCode(refactors)})    
        neighbour = createNeighborhood(refactors,1)[0]

        refactor = random.choice(neighbour)
        haskellFile = applyRefactor(haskellFile,refactor,str(i))

        i = i + 1
        if i == maxIterations:
            break


# Inicia el templado simulado.
def initSimulatedAnnealing(haskellFile,maxTemp,deltaTemp):
    
    minTemp = 1
    currentTemp = maxTemp

    while True:
        refactors = prioritizeRefactors(parseFile(haskellFile),False)
        codeEval.append({"file": haskellFile,"quality": evaluateCode(refactors)})
        currentNeighbour = createNeighborhood(refactors, 1)[0]
        
        refactor = random.choice(currentNeighbour)

        newRefactor = mutateRefactor(refactor)
        
        s = applyRefactor(haskellFile,refactor,'current')
        sNew = applyRefactor(haskellFile,newRefactor,'new')

        sFit = evaluateCode(prioritizeRefactors(parseFile(s),False))
        sNewFit = evaluateCode(prioritizeRefactors(parseFile(sNew),False))

        delta = sFit - sNewFit
        
        if delta >= 0:
            haskellFile = sNew
            quality = sNewFit
        else:
            if random.random() < math.exp(-abs(delta)/currentTemp):
                haskellFile = sNew
                quality = sNewFit
            else:
                haskellFile = s
                quality = sFit
        
        currentTemp = currentTemp - deltaTemp

        if currentTemp < minTemp:
            break

# Elimina las carpetas intermedias creadas en el directorio que se le pase. 
def deleteIntermediateFolders(folder):
    subprocess.run("rm -rf " + folder + "-*",stdout=subprocess.PIPE,shell=True)

# Copia el ultimo archivo agregado a la variable codeEval al directorio del archivo que se quiere refactorizar con el numero de la iteracion.
def copyFile(codeEvalFile,refactorFileLocalization,iteration):
    fileLocalization,fullFileName,fileName,extension = extractFileFeatures(refactorFileLocalization)
    subprocess.run("cp " + os.path.realpath(codeEvalFile) + " " + fileLocalization + fileName + '-' + str(iteration)  + "-refactored" + extension ,stdout=subprocess.PIPE,shell=True)

### MAIN FUNCTION ###

def main():
    parser = argparse.ArgumentParser(description='Tool for Haskell Code Refactoring')
    parser.add_argument("--file", type=str, required=True, help="file to refactor")
    parser.add_argument("--iterations", default=1, type=int, required=True, help="number of iterations")
    parser.add_argument("--type", choices=["SA", "interactive","random"], required=True, type=str, help="refactor mode")
    parser.add_argument("--maxTemp", default=20, type=int, help="max temperature in simulated annealing (default = 20)")
    parser.add_argument("--deltaTemp", default=3, type=int, help="decrease of temperature in simulated annealing (default = 3)")
    parser.add_argument("--maxIterations", default=5, type=int, help="max iterations in random search method (default = 5)")
    interFiles_parser = parser.add_mutually_exclusive_group(required=False)
    interFiles_parser.add_argument('--intermediate-folders', dest='interFolders', action='store_true', help="save intermediate folders")
    interFiles_parser.add_argument('--no--intermediate-folders', dest='interFolders', action='store_false', help="don't save intermediate folders")
    parser.set_defaults(feature=False)

    args = parser.parse_args()
    numIterations = args.iterations

    refactorFileLocalization = os.path.realpath(args.file)
    
    global codeEval
    
    if args.type == 'interactive':
        for iteration in range(0,numIterations):
            print("Manual - Iteration number: " + str(iteration))
            initManualRefactoring(args.file)
            copyFile(codeEval[-1]['file'],refactorFileLocalization,iteration)
            print(codeEval)
            codeEval = []
    
    elif args.type == 'SA':
        for iteration in range (0,numIterations):
            print("SA - Iteration number: " + str(iteration))
            initSimulatedAnnealing(args.file,args.maxTemp,args.deltaTemp)
            copyFile(getBestQuality(codeEval),refactorFileLocalization,iteration)
            print(codeEval)
            codeEval = []
    
    elif args.type == 'random':
        for iteration in range (0,numIterations):
            print("Random - Iteration number: " + str(iteration))
            initRandomRefactoring(args.file,args.maxIterations)
            copyFile(codeEval[-1]['file'],refactorFileLocalization,iteration)
            print(codeEval)
            codeEval = []
    
    if args.interFolders == False:
        deleteIntermediateFolders(os.path.dirname(refactorFileLocalization))
        print("Deleting intermediate folders.")
    else:
        print("Preserving intermediate folders.")
        
if __name__ == "__main__":
    main()

