__author__ = "Baley R. and Labeye L."
__email__ = ["romain.baley@groupe-esigelec.org", "loic.labeye@groupe-esigelec.org"]

import timeit
import sys
import argparse
import os
import string
import random
import hashlib as hl
import matplotlib.pyplot as plt

def get_hash(algo: str, message: str) -> str:
    """
    Get hash of the given alg for the given arg
    """
    return getattr(hl, algo)(message.encode('utf8'))


def time_hash_computation(algo: str, message: str, iters: int) -> float:
    """
    Time the hash computation for the program
    """
    return timeit.Timer(
        lambda:
            get_hash(algo, message).hexdigest()
    ).timeit(iters)/iters


def output_in_console(results_to_display : dict) -> None:
    """
    Writes the output in the console
    """
    for index, message in enumerate(results_to_display):
        print(f"\n---\nArg {index}: {message['value']}")
        for alg in message['algs']:
            print(f"* {alg['name']}: {alg['hash_digest']}")
            print(f"\t-Digest size : {alg['digest_size']}")
            print(f"\t-Block size : {alg['digest_bs']}")
            print(f"\t-Average time for {message['trials']} : {alg['avgtime']}")


def write_aggregate_results(results_to_aggregate : dict) -> None:
    """
    Show aggregate results per algorithms
    """
    # Sort by length of the key
    sorted_results = sorted(results_to_aggregate, key=lambda result: len(result['value']))
    for index, alg in enumerate(results[0]['algs']):
        vals = []
        plt.title('Difference of time to compute for different sizes')
        for result in sorted_results:
            vals.append((result['length'], result['algs'][index]['avgtime']))
        plt.plot(
            [int(x[0]) for x in vals],
            [float(y[1]) for y in vals], label=f'{alg["name"]}'
        )
        plt.xlabel("Length of the key")
        plt.ylabel("Time in s")
        plt.legend()
        plt.savefig(f'reports{os.sep}diffs.png')

    plt.clf()
    plt.style.use('ggplot')
    vals = sorted(
        [(alg['name'], alg['digest_size'])  for alg in sorted_results[0]['algs']],
        key=lambda value: value[1]
    )
    plt.bar([x[0] for x in vals], [y[1] for y in vals], color='green')
    plt.xlabel("Algorithm")
    plt.ylabel("Digest size")
    plt.title("Difference of digest size per algorithms")
    plt.savefig(f'reports{os.sep}ds.png')
    plt.clf()

    plt.style.use('ggplot')
    vals = sorted(
        [(alg['name'], alg['digest_bs'])  for alg in sorted_results[0]['algs']],
        key=lambda value: int(value[1])
    )
    plt.bar([x[0] for x in vals], [y[1] for y in vals], color='blue')
    plt.xlabel("Algorithm")
    plt.ylabel("Digest bloc size")
    plt.title("Difference of block size per algorithms")
    plt.savefig(f'reports{os.sep}bs.png')
    plt.clf()

    with open(f'reports{os.sep}compare_results.md', 'w') as file:
        algs_names = [alg['name'] for alg in sorted_results[0]['algs']]
        file.write(f"# Comparison of time differences for the algs : {', '.join(algs_names)}\n")
        file.write(f"{'|'.join(['Length']+algs_names)}\n")
        file.write("|".join(["-" for i in range(len(sorted_results[0]['algs'])+1)]))
        file.write("\n")
        for result in sorted_results:
            file.write("|".join([str(len(result['value']))]+[
                str(alg['avgtime']) for alg in result['algs']
            ]))
            file.write("\n")
        file.write("\n")
        file.write("![Difference between the algorithms](ds.png)\n")
        file.write("![Difference between the algorithms](bs.png)\n")
        file.write("![Difference between the algorithms](diffs.png)\n")

def get_args():
    """
    Get args value from the cmd line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs',
        metavar='number_of_random_str',
        nargs='?',
        default=[],
        type=int,
        help='number of random strings to be hashed'
    )
    parser.add_argument("--iters",
        "-i",
        metavar='i',
        default=10000,
        type=int,
        help="number of iterations"
    )
    parser.add_argument("--algs",
        "-a",
        type=str,
        default=['sha256', 'md5'],
        nargs='+',
        help="algorithms to try"
    )
    parser.add_argument("--silent",
        "-s",
        nargs='?',
        type=bool,
        default=False,
        const=True,
        help="define if the result is printed in console"
    )
    args = parser.parse_args()

    if args.inputs:
        argv = [''.join([
                random.choice(string.ascii_letters) for j in range(i)
            ]) for i in range(args.inputs)]
    else:
        print("Provide arguments")
        sys.exit()

    return argv, args.iters, args.algs, args.silent


if __name__ == "__main__":
    random_string_array, nb_trials, algs, silent = get_args()
    results = []
    for arg in random_string_array:
        results.append({})
        current_arg = results[len(results)-1]
        current_arg['value'] = arg
        current_arg['length'] = len(arg)
        current_arg['trials'] = nb_trials
        current_arg['algs'] = []
        for algorithm in algs:
            digest = get_hash(algorithm, arg)
            time_for_hash = time_hash_computation(algorithm, arg, int(nb_trials))
            current_arg['algs'].append({
                "name":str(algorithm),
                "digest_bs":str(digest.block_size),
                "digest_size":str(digest.digest_size),
                "hash_digest":str(digest.hexdigest()),
                "avgtime":str(time_for_hash)
            })
    if not silent:
        output_in_console(results)

    write_aggregate_results(results)
