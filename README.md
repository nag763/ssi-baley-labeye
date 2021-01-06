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
python baley_labeye_ssi.py --help
usage: baley_labeye_ssi.py [-h] [--iters i] [--random r]
                           [--algs ALGS [ALGS ...]] [--output [OUTPUT]]
                           [--silent [SILENT]] [--compare [COMPARE]]
                           value [value ...]

positional arguments:
  value                 arguments to be hashed

optional arguments:
  -h, --help            show this help message and exit
  --iters i, -i i       number of iterations
  --random r, -r r      number of random elements
  --algs ALGS [ALGS ...], -a ALGS [ALGS ...]
                        algorithms to try
  --output [OUTPUT], -o [OUTPUT]
                        define if an output is required
  --silent [SILENT], -s [SILENT]
                        define if the result is printed in console
  --compare [COMPARE], -c [COMPARE]
                        define if a comparison between the output has to be
                        saved
```

## Exemples

### Write the output in cmd line

```
python baley_labeye_ssi example hello
```

### Save the output in report folder

```
python baley_labeye_ssi example hello -o
```

### Save the comparison between the algorithms in a file

```
python baley_labeye_ssi example hello -c
```

### Use random inputs, and compare them

```
python baley_labeye_ssi random -r 128 -c
```

### Don't print the output of the commands in the terminal

```
python baley_labeye_ssi random -r 128 -c --silent
```

### Use fewer trials than the default one

```
python baley_labeye_ssi random -r 128 -c -i 120
```
