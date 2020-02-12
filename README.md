# haskell-refactor-tool
A python tool for haskell code refactoring. This is a prototype which was done in the context of an research on automatic code refactoring for the GICCIS group.

## Features
### Dependencies
This tool uses two main external libraries. 
* Homplexity (https://github.com/migamake/homplexity) for measuring quality of the code.
* Haskell-Tools (https://github.com/haskell-tools/haskell-tools/) for applying the refactors with the tool HT-Refact.

### Modes 
Two main modes:
* Manual. Accept or deny a sorted list of refactors manually.
* SA (Simulated Annealing). Automatic code refactor using SA algorithm. (Still not done)

### Limits.
* Can only refactor a few types of code-smells.

## Usage
We have created a Dockerfile that contains the exact versions of the libraries required for running this script. 

### Building the image
```
docker build . -t refactor-image
```

### Using the container (example).
Mount a volume that contains both the code you want to refactor and all the scripts in this repository.
```
docker run -v ~/code:/code -ti refactor-image  /bin/bash
cd code
python3 main.py --file haskell/Main1.hs --iterations 1 --type manual --maxTemp 50
```
