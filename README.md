# haskell-refactor-tool
This is a prototype which was done in the context of a research on automatic code refactoring for the GIICIS group. 

## Features
### Libraries
This tool uses two main external libraries. 
* [Homplexity](https://github.com/migamake/homplexity) for measuring quality of the code.
* [Haskell-Tools](https://github.com/haskell-tools/haskell-tools/) for applying the refactors with the tool HT-Refact.

### Modes 
Two main modes:
* Interactive. Accept or deny a sorted list of refactors manually.
* SA (Simulated Annealing). Automatic code refactor using SA algorithm. (Not completed)
* Random. Automatic code Refactor using random algorithm.

### Limits.
* Can only refactor a few types of code-smells. This is caused because there aren't a lot of posible refactors. However this can be fixed if other tool is used or developing new refactors for Haskell-Tools.
* Refactor one file at the time.

## Usage
We have created a Dockerfile that contains the exact versions of the libraries required for running this script and it's uploaded to this repository. 

### Building the image
```
docker build . -t refactor-image
```

### Using the container (example).
Mount a volume that contains both the code you want to refactor and all the scripts in this repository. 
```
docker run -v ~/code:/code -ti refactor-image  /bin/bash
cd code
python3 main.py --file haskell/Main1.hs --iterations 1 --type manual --maxTempIterations 50
```

This is not ideal. The building process can take some time and the builded image is heavy but it's a temporary solution that we have used. We will improve this.
