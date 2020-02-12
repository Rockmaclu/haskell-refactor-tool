import json

# Funcion de evaluacion de calidad de codigo. Devuelve un entero con un numero que representa la calidad. Cuanto mas cercano a 0 esten los valores, mayor sera la calidad.
def evaluateCode(listOfRefactors):
    
    listOfRefactors = json.loads(listOfRefactors)

    # Good code -> Close to 0
    # Bad code -> Far from 0 
    codeQuality = 0

    for refactor in listOfRefactors: 
        codeQuality = refactor['nPriority'] + codeQuality
    
    return codeQuality


