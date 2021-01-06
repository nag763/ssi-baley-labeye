__author__ = "Baley R. and Labeye L."
__email__ = ["romain.baley@groupe-esigelec.org", "loic.labeye@groupe-esigelec.org"]

import hashlib as hl
import timeit
import csv2md
import sys
import re
import argparse
import os

def getHash(alg: str, arg: str) -> str :
    """
    Get hash of the given alg for the given arg
    """
    return getattr(hl, alg)(arg.encode('utf8'))


def time_hash_computation(alg: str, arg: str, iters: int):
    """
    Time the hash computation for the program
    """
    return timeit.Timer(lambda:getHash(algorithm, arg).hexdigest()).timeit(iters)/iters


def password_score(password : str) -> int:
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """
    # calculating the length
    length_acceptable = len(password) > 8
    # searching for digits
    digit_acceptable = re.search(r"\d", password) is not None
    # searching for uppercase
    uppercase_acceptable = re.search(r"[A-Z]", password) is not None
    # searching for lowercase
    lowercase_acceptable = re.search(r"[a-z]", password) is not None
    # searching for symbols
    symbol_acceptable = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is not None
    return length_acceptable + digit_acceptable + uppercase_acceptable + lowercase_acceptable + symbol_acceptable


def get_args():
    """
    Get args value from the cmd line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', metavar='value', type=str, nargs='+', help='arguments to be hashed')
    parser.add_argument("--iters", "-i", metavar='i', default=10000, type=int, help="number of iterations")
    parser.add_argument("--algs", "-a", type=str, default=['sha256', 'md5'], nargs='+', help="algorithms to try")
    parser.add_argument("--output", "-o", nargs='?', type=bool, default=False, const=True, help="define if an output is required")
    args = parser.parse_args()
    if args.inputs:
        argv = args.inputs
    else:
        print("Provide arguments")
        sys.exit()

    return argv, args.iters, args.algs, args.output


if __name__ == "__main__":
    argv, iters, algs, write_in_file = get_args()
    for index, arg in enumerate(argv) :
        score = password_score(arg)
        output = []
        output.append(f"# Comparison for {arg}")
        output.append("")
        output.append(f"Score of the argument : {score}/5")
        output.append(f"Number of trials for each hash : {iters}")
        output.append("|".join(["Algorithm","Hash","Digest size","Block size","Time"]))
        output.append("|".join("-" for i in range(5)))
        print(f"\n---\nArg {index} : {arg}\t Score : {score} /5")
        for algorithm in algs:
            hash = getHash(algorithm, arg)
            time_for_hash = time_hash_computation(algorithm, arg, int(iters))
            print(f"* {algorithm}: {hash.hexdigest()}")
            print(f"\t-Digest size : {hash.digest_size}")
            print(f"\t-Block size : {hash.block_size}")
            print(f"\t-Average time for {iters} : {time_for_hash}")
            output.append(f"{algorithm}|{hash.hexdigest()}|{hash.digest_size}|{hash.block_size}|{time_for_hash}")
            if write_in_file:
                with open(f'reports{os.path.sep}{arg}.md', 'w') as f:
                    for line in output:
                        f.write(f'{line}\n')
