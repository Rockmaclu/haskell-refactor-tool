import random
import copy

# Lista de posibles acciones a realizar en cada refactorizacion.
posibleRefactors = ["ExtractBinding","InlineBinding","NoRefactor"]

# Asigna aleatoriamente al conjunto de posibles refactorizaciones una accion determinada.
def createNeighborhood(refactors,n):
    listOfNeighbours = []
    for i in range(0,n):
        neighbour = []
        for refactor in refactors:
            newRefactor = copy.deepcopy(refactor)
            newRefactor['pRefactor'] = random.choice(posibleRefactors)
            neighbour.append(newRefactor)
        listOfNeighbours.append(neighbour)

    return listOfNeighbours

# Cambia aleatoramiente la accion de una posible refactorizacion dentro del vecindario.
def mutateNeighbour(neighbour):
    pos = random.randint(0,len(neighbour)-1)
    auxPosibleRefactors = copy.deepcopy(posibleRefactors)
    auxPosibleRefactors.remove(neighbour[pos]['pRefactor'])
    neighbour[pos]['pRefactor'] = random.choice(auxPosibleRefactors) 

    return neighbour

# Cambia aleatoriamente la accion de una refactorizacion.
def mutateRefactor(refactor):
    auxPosibleRefactors = copy.deepcopy(posibleRefactors)
    auxPosibleRefactors.remove(refactor['pRefactor'])
    auxRefactor = copy.deepcopy(refactor)
    auxRefactor['pRefactor'] = random.choice(auxPosibleRefactors)
    return auxRefactor 

