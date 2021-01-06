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


def write_each_result(results):
    for current_result in results: 
        with open(f'reports{os.sep}{current_result["value"]}.md', 'w') as f:
            f.write(f"# Comparison for {current_result['value']}\n")
            f.write("\n")
            f.write(f"Score of the argument : {current_result['score']}/5\n")
            f.write(f"Number of trials for each hash : {current_result['trials']}\n")
            f.write(f"Length of the argument : {current_result['length']}\n")
            f.write("|".join(["Algorithm","Hash","Digest size","Block size","Time"]))
            f.write("\n")
            f.write("|".join(["-" for i in range(5)]))
            f.write("\n")
            for alg in current_result['algs']:
                f.write(f"{alg['name']}|{alg['hash_digest']}|{alg['digest_size']}|{alg['digest_bs']}|{alg['avgtime']}")
                f.write("\n")


def output_in_console(results):
    for index, arg in enumerate(results):
        print(f"\n---\nArg {index}: {arg['value']}\t Score : {arg['score']} /5")
        for alg in arg['algs']:
            print(f"* {alg['name']}: {alg['hash_digest']}")
            print(f"\t-Digest size : {alg['digest_size']}")
            print(f"\t-Block size : {alg['digest_bs']}")
            print(f"\t-Average time for {arg['trials']} : {alg['avgtime']}")


def get_args():
    """
    Get args value from the cmd line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', metavar='value', type=str, nargs='+', help='arguments to be hashed')
    parser.add_argument("--iters", "-i", metavar='i', default=10000, type=int, help="number of iterations")
    parser.add_argument("--algs", "-a", type=str, default=['sha256', 'md5'], nargs='+', help="algorithms to try")
    parser.add_argument("--output", "-o", nargs='?', type=bool, default=False, const=True, help="define if an output is required")
    parser.add_argument("--silent", "-s", nargs='?', type=bool, default=False, const=True, help="define if the result is printed in console")
    args = parser.parse_args()
    if args.inputs:
        argv = args.inputs
    else:
        print("Provide arguments")
        sys.exit()

    return argv, args.iters, args.algs, args.output, args.silent


if __name__ == "__main__":
    argv, iters, algs, write_in_file, silent = get_args()
    results = []
    for index, arg in enumerate(argv) :
        score = password_score(arg)
        results.append({})
        current_arg = results[len(results)-1]
        current_arg['value'] = arg
        current_arg['length'] = len(arg)
        current_arg['score'] = score
        current_arg['trials'] = iters
        current_arg['algs'] = []
        for algorithm in algs:
            hash = getHash(algorithm, arg)
            time_for_hash = time_hash_computation(algorithm, arg, int(iters))
            current_arg['algs'].append({
                "name":str(algorithm),
                "digest_bs":str(hash.block_size),
                "digest_size":str(hash.digest_size),
                "hash_digest":str(hash.hexdigest()),
                "avgtime":str(time_for_hash)
                })
    if not silent:
        output_in_console(results)
    if write_in_file:
        write_each_result(results)
