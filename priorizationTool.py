import yaml

# Lista de errores posibles detectables por la herramienta Homplexity (algunos no funcionan bien).
errorTypes = ["nil","constructor depth","arguments","lines of code","lines of code","conditionals","cyclomatic complexity"]

# Array global con el peso de los distintos errores.
errorWeights = []

# A partir del mensaje de error que arroja Homplexity cuando se hace un escaneo del codigo se identifica a cual pertenece.
def defineError(errorString):
    for i,error in enumerate(errorTypes):
        if error in errorString:
            return i
    return 0

# Se define una prioridad de la refactorizacion en base a su criticidad y al tipo de error segun lo que defina el usuario.
def definePriority(refactor):
    nPriority = 0
    if (refactor['priority'] == 'Warning'):
        nPriority = errorWeights[0]
    else:
        nPriority = errorWeights[1]
    indexError = defineError(refactor['error'])

    refactor['errorName'] = errorTypes[indexError]
    refactor['nPriority'] = nPriority * errorWeights[indexError+1]
    
    return refactor

# Funcion que carga los pesos del archivo config a un arreglo en el programa.
def loadWeights():
    with open("config.yaml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
    errorWeights.append(cfg['priorizationToolWeight']['warning'])
    errorWeights.append(cfg['priorizationToolWeight']['critical'])
    errorWeights.append(cfg['priorizationToolWeight']['constructorDepth'])
    errorWeights.append(cfg['priorizationToolWeight']['numFunctionArguments'])
    errorWeights.append(cfg['priorizationToolWeight']['moduleLine'])
    errorWeights.append(cfg['priorizationToolWeight']['functionLine'])
    errorWeights.append(cfg['priorizationToolWeight']['functionDepth'])
    errorWeights.append(cfg['priorizationToolWeight']['functionCC'])

# Funcion que prioriza las refactorizaciones y puede devolverlas o no ordenadas segun su prioridad.
def prioritizeRefactors(refactors,sort):
    loadWeights()
    for refactor in refactors:
        refactor = definePriority(refactor) 
    if sort == True:
        return sorted(refactors, key=lambda k: k['nPriority'],reverse=True)
    else:
        return refactors
    
