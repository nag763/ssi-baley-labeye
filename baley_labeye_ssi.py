__author__ = "Baley R. and Labeye L."
__email__ = ["romain.baley@groupe-esigelec.org", "loic.labeye@groupe-esigelec.org"]

import hashlib as hl
import timeit
import sys
import re
import argparse
import os
import matplotlib.pyplot as plt
import string
import random


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


def output_in_console(results):
    """
    Writes the output in the console
    """
    for index, arg in enumerate(results):
        print(f"\n---\nArg {index}: {arg['value']}")
        for alg in arg['algs']:
            print(f"* {alg['name']}: {alg['hash_digest']}")
            print(f"\t-Digest size : {alg['digest_size']}")
            print(f"\t-Block size : {alg['digest_bs']}")
            print(f"\t-Average time for {arg['trials']} : {alg['avgtime']}")


def show_aggregate_results(results):
    """
    Show aggregate results per algorithms
    """
    # Sort by length of the key
    results = sorted(results, key=lambda result: len(result['value']))
    for index, alg in enumerate(results[0]['algs']):
        vals = []
        plt.title(f'Difference of time to compute for different sizes')
        for result in results:
            vals.append((result['length'], result['algs'][index]['avgtime']))
        plt.plot([int(x[0]) for x in vals], [float(y[1]) for y in vals], label=f'{alg["name"]}')
        plt.xlabel("Length of the key")
        plt.ylabel("Time in s")
        plt.legend()
        plt.savefig(f'reports{os.sep}diffs.png')

    plt.clf()
    plt.style.use('ggplot')
    vals = sorted([(alg['name'], alg['digest_size'])  for alg in results[0]['algs']], key=lambda value: value[1])
    plt.bar([x[0] for x in vals], [y[1] for y in vals], color='green')
    plt.xlabel("Algorithm")
    plt.ylabel("Digest size")
    plt.title("Difference of digest size per algorithms")
    plt.savefig(f'reports{os.sep}ds.png')
    plt.clf()

    plt.style.use('ggplot')
    vals = sorted([(alg['name'], alg['digest_bs'])  for alg in results[0]['algs']], key=lambda value: int(value[1]))
    plt.bar([x[0] for x in vals], [y[1] for y in vals], color='blue')
    plt.xlabel("Algorithm")
    plt.ylabel("Digest bloc size")
    plt.title("Difference of block size per algorithms")
    plt.savefig(f'reports{os.sep}bs.png')
    plt.clf()

    with open(f'reports{os.sep}compare_results.md', 'w') as f:
        f.write(f"# Comparison of time differences for the algs : {', '.join([alg['name'] for alg in results[0]['algs']])}\n")
        f.write(f"{'|'.join(['Length']+[alg['name'] for alg in results[0]['algs']])}\n")
        f.write("|".join(["-" for i in range(len(results[0]['algs'])+1)]))
        f.write("\n")
        for result in results:
            f.write("|".join([str(len(result['value']))]+[str(alg['avgtime']) for alg in result['algs']]))
            f.write("\n")
        f.write("\n")
        f.write("![Difference between the algorithms](ds.png)\n")
        f.write("![Difference between the algorithms](bs.png)\n")
        f.write("![Difference between the algorithms](diffs.png)\n")

def get_args():
    """
    Get args value from the cmd line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', metavar='number_of_random_str', nargs='?', default=[], type=int, help='number of random strings to be hashed')
    parser.add_argument("--iters", "-i", metavar='i', default=10000, type=int, help="number of iterations")
    parser.add_argument("--algs", "-a", type=str, default=['sha256', 'md5'], nargs='+', help="algorithms to try")
    parser.add_argument("--silent", "-s", nargs='?', type=bool, default=False, const=True, help="define if the result is printed in console")
    args = parser.parse_args()

    if args.inputs:
        argv = [''.join([random.choice(string.ascii_letters) for j in range(i)]) for i in range(args.inputs)] 
    else:
        print("Provide arguments")
        sys.exit()

    return argv, args.iters, args.algs, args.silent


if __name__ == "__main__":
    argv, iters, algs, silent = get_args()
    results = []
    for index, arg in enumerate(argv) :
        results.append({})
        current_arg = results[len(results)-1]
        current_arg['value'] = arg
        current_arg['length'] = len(arg)
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

    show_aggregate_results(results) 
