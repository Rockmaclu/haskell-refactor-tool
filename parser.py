import json
import re
import subprocess
import yaml

# Variable que contiene la estructura de una refactorizacion.
headers = ("priority","srcMod","srcLoc","line","error","errorName","nPriority","pRefactor","nFunction")

# Parsea un String de refactorizacion y devuelve una refactorizacion con formato json.
def parseLine(line):
    aux = re.split(':|\" | \"',line)
    del aux[2]
   
    aux.append("undefine")
    aux.append(0)
    aux.append("none")
    errorAux = aux[4].split()
    if errorAux[0] == "function":
        aux.append(errorAux[1])
    else:
        aux.append("NULL")
    aux[3] = aux[3].replace(" ",":")

    return dict(zip(headers, aux))
    
# Parsea una lista de refactorizaciones y devuelve un json con todas las refactorizaciones creadas.
def parseList(listCodeSmells):
    result = []
    for codeSmell in listCodeSmells:
        result.append(parseLine(codeSmell))
    return json.dumps(result,indent=4)

# Parsea un string con todas las refactorizaciones y lee cada una de las lineas. Luego se las pasa al parseador de listas.
def parseDocument(refactors):
    lineList = [] 
    for line in refactors.splitlines():
        lineList.append(line)
    del lineList[-1]
    return parseList(lineList)

# Ejecuta la libreria de Homplexity teniendo en cuenta los pesos de configuracion y extrae donde hay code-smells en el archivo.
def runHomplexity(haskellFile,severity):
    
    arguments = ["/root/.local/bin/homplexity-cli"]
    arguments.append(haskellFile)
    
    with open("config.yaml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    arguments.append("--severity="+severity)
    value = 1000000
    # Se divide en criticidad debido a un bug que existe en la libreria Homplexity que no detecta code-smells criticos.
    if severity == "Critical":
        arguments.append("--typeConDepthWarning="+str(value))
        arguments.append("--typeConDepthCritical="+str(cfg['homplexityArguments']['constructorDepthC']))
        arguments.append("--numFunArgsWarning="+str(value))
        arguments.append("--numFunArgsCritical="+str(cfg['homplexityArguments']['numFunctionArgumentsC']))
        arguments.append("--moduleLinesWarning="+str(value))
        arguments.append("--moduleLinesCritical="+str(cfg['homplexityArguments']['moduleLinesC']))
        arguments.append("--functionLinesWarning="+str(value))
        arguments.append("--functionLinesCritical="+str(cfg['homplexityArguments']['functionLineC']))
        arguments.append("--functionDepthWarning="+str(value))
        arguments.append("--functionDepthCritical="+str(cfg['homplexityArguments']['functionDepthC']))
        arguments.append("--functionCCWarning="+str(value))
        arguments.append("--functionCCCritical="+str(cfg['homplexityArguments']['functionCCC']))
    else: 
        arguments.append("--typeConDepthWarning="+str(cfg['homplexityArguments']['constructorDepthW']))
        arguments.append("--typeConDepthCritical="+str(value))
        arguments.append("--numFunArgsWarning="+str(cfg['homplexityArguments']['numFunctionArgumentsW']))
        arguments.append("--numFunArgsCritical="+str(value))
        arguments.append("--moduleLinesWarning="+str(cfg['homplexityArguments']['moduleLinesW']))
        arguments.append("--moduleLinesCritical="+str(value))
        arguments.append("--functionLinesWarning="+str(cfg['homplexityArguments']['functionLineW']))
        arguments.append("--functionLinesCritical="+str(value)) 
        arguments.append("--functionDepthWarning="+str(cfg['homplexityArguments']['functionDepthW']))
        arguments.append("--functionDepthCritical="+str(value))
        arguments.append("--functionCCWarning="+str(cfg['homplexityArguments']['functionCCW']))
        arguments.append("--functionCCCritical="+str(value))
    
    resultado = subprocess.run(arguments,stdout=subprocess.PIPE)
    return resultado.stdout.decode('utf-8')

# Se encarga de extraer todos los code-smells del archivo que se le pasa y devuelve un json ordenado de los mismos.
def parseFile(fileLocalization):
    criticalRefactors = json.loads(parseDocument(runHomplexity(fileLocalization,"Critical")))
    warningRefactors = json.loads(parseDocument(runHomplexity(fileLocalization,"Warning")))
    
    if len(criticalRefactors) != 0:
        for criticalRefactor in criticalRefactors:
            for warningRefactor in warningRefactors:
                if criticalRefactor['line'] == warningRefactor['line']:
                    warningRefactors = list(filter(lambda i: i['line'] != warningRefactor['line'], warningRefactors)) 
                    break;
                
    refactors = json.dumps(criticalRefactors + warningRefactors,indent=4)

    return refactors
