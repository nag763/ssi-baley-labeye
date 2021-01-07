# Lab work for the SSI course at ESIGELEC - BALEY; LABEYE

The purpose of this program is to evaluate quickly the main differences between the different hash algorithms.

![example](usage.gif)

## How to install

1. (Optional) You should create a virtual env

```bash
python -m venv .env
```

2. You activate your virtual env

Linux

```bash
source .env/bin/activate
```

3. You install the required dependencies

```bash
pip install -r requirements.txt
```

4. Once the dependencies installed, you can use the program !

```bash
python baley_labeye_ssi.py
```

## Commands

```
$ python baley_labeye_ssi.py --help
usage: baley_labeye_ssi.py [-h] [--iters i] [--algs ALGS [ALGS ...]]
                           [--silent [SILENT]]
                           [number_of_random_str]

positional arguments:
  number_of_random_str  number of random strings to be hashed

optional arguments:
  -h, --help            show this help message and exit
  --iters i, -i i       number of iterations
  --algs ALGS [ALGS ...], -a ALGS [ALGS ...]
                        algorithms to try
  --silent [SILENT], -s [SILENT]
                        define if the result is printed in console
```

## Exemples

### Use 12 random inputs with a size from 0 to 11, and compare them

```
python baley_labeye_ssi.py 12
```

### Use only sha256 algorithm for 12 random inputs with a size from 0 to 11

```
python baley_labeye_ssi.py 12 -a sha256
```

### Use only sha256 algorithm for 12 random inputs with a size from 0 to 11, and 100 trials for each hash

```
python baley_labeye_ssi.py 12 -a sha256 -i 100
```

### Don't print the result of the commands in the terminal

```
python baley_labeye_ssi.py 12 --silent
```
