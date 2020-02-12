import difflib

# Imprime en pantalla las diferencias entre dos archivos. 
def printCodeDifference(file1,file2):
    text1 = open(file1).readlines()
    text2 = open(file2).readlines()
    
    diffs = difflib.context_diff(text1, text2)
    for line in diffs:
        print(line)
