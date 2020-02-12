import subprocess
import os
import random
from visualization import *

# Argumento principal que utilizamos para ejecutar la libreria HT-Refact.
mainargument = "stack exec -- /root/.local/bin/ht-refact -e"

# Funcion auxiliar que crea la cadena de ejecucion correspondiente a cada posible refactorizacion.
def createExecString(refactor,auxFile):
    if refactor["pRefactor"] == "ExtractBinding":
        return refactor["pRefactor"] + " " + auxFile + " " +  refactor["line"] + " " + refactor["nFunction"] + "1"
    if refactor["pRefactor"] == "InlineBinding":
        return refactor["pRefactor"] + " " + auxFile + " " + refactor["line"]
    if refactor["pRefactor"] == "NoRefactor":
        return ""

# Funcion auxiliar que extrae en distintas variables la localizacion de un archivo, el nombre completo, luego su nombre y luego su extension. 
def extractFileFeatures(haskellFile):
    fileLocalization = os.path.dirname(haskellFile)
    fullFileName = os.path.basename(haskellFile)
    fileName = "/"+os.path.splitext(fullFileName)[0]
    extension = os.path.splitext(fullFileName)[1]

    return fileLocalization,fullFileName,fileName,extension

# Funcion auxiliar que ejecuta los comandos para crear una carpeta, copiar el archivo nuevo creado y elimina el cache temporal creado.
def executeFileCommands(newFileLocalization,auxFile,fullFileName,fileLocalization,i):
    subprocess.run("mkdir -p " + newFileLocalization,stdout=subprocess.PIPE,shell=True)
    subprocess.run("cp " + auxFile + " " + newFileLocalization + "/" + fullFileName,stdout=subprocess.PIPE,shell=True)
    subprocess.run("rm -rf " + fileLocalization + "/cache*",stdout=subprocess.PIPE,shell=True)

# Funcion principal que se encarga de aplicar una refactorizacion utilizando la libreria HT-Refact. Esta se utiliza cuando el modo esta en SA.
def applyRefactor(haskellFile,refactor,i):
    fileLocalization,fullFileName,fileName,extension = extractFileFeatures(haskellFile)
    auxFile = fileLocalization + "/cache"+ i + fileName + extension
    
    subprocess.run("mkdir -p " +fileLocalization + "/cache" + i,stdout=subprocess.PIPE,shell=True)
    subprocess.run("cp " + haskellFile + " " + auxFile,stdout=subprocess.PIPE,shell=True)
   
    execString = createExecString(refactor,auxFile)
    if execString != "":
        result = (subprocess.run(mainargument + " \"" + execString + "\" " + fileLocalization+"/cache"+i,stdout=subprocess.PIPE,shell=True)).stdout
    
    newFileLocalization = fileLocalization + "-" + i

    executeFileCommands(newFileLocalization,auxFile,fullFileName,fileLocalization,i)
    
    return newFileLocalization + "/" + fullFileName
    
# Funcion principal que se encarga de copiar el archivo refactorizado a su nueva carpeta. Este se utiliza cuando el modo esta en manual.
def copyRefactor(haskellFile,i):
    fileLocalization,fullFileName,fileName,extension = extractFileFeatures(haskellFile)
    auxFile = fileLocalization +"/cache"+ fileName + extension
    
    newFileLocalization = fileLocalization + "-" + i
     
    executeFileCommands(newFileLocalization,auxFile,fullFileName,fileLocalization,i)

    return newFileLocalization + "/" + fullFileName

# Funcion principal que se encarga de mostrar la refactorizacion a aplicar. Esta se utiliza cuando el modo esta en manual.
def seeRefactor(haskellFile,refactor):
    fileLocalization,fullFileName,fileName,extension = extractFileFeatures(haskellFile)
    auxFile = fileLocalization + "/cache" + fileName + extension
    
    subprocess.run("mkdir -p " +fileLocalization + "/cache",stdout=subprocess.PIPE,shell=True)
    subprocess.run("cp " + haskellFile + " " + auxFile,stdout=subprocess.PIPE,shell=True)
    
    execString = createExecString(refactor,auxFile)
    if execString == "":
        return True
    result = (subprocess.run(mainargument + " \"" + execString + "\" " + fileLocalization+"/cache",stdout=subprocess.PIPE,shell=True)).stdout
    
    if (b'Loaded module:'  in result.splitlines()[-1]):
        printCodeDifference(haskellFile, auxFile)
        return False

    return True

