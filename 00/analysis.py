import argparse
import json
import multiprocessing
import os

import matplotlib.pyplot as plt
from tqdm import tqdm

def get_hash_table(hash_file):
    with open(hash_file, 'r') as json_file:
        table = json.load(json_file)
    # print(list(table.items())[:10])

    # filter hash with len > 1
    table = {key: value for key, value in tqdm(table.items()) if len(value) > 1}
    # print(list(table.items())[:10])
    return table

def analysis_one_entry(entry):
    freq = {}
    for i, a in enumerate(entry):
        for b in entry[i+1:]:
            v = b-a
            if v not in freq:
                freq.update({v:0})
            freq[v] += 1
    return freq

def analysis(hash_file):
    table = get_hash_table(hash_file)
    print(f"table size: {len(table)}")

    pool = multiprocessing.Pool()
    results = [pool.apply_async(analysis_one_entry, (value,)) for value in tqdm(table.values())]

    final_results = {}
    for result in tqdm(results):
        tmp = result.get()
        for key,val in tmp.items():
            if key not in final_results:
                final_results.update({key:0})
            final_results[key] += val
    # print(final_results)

    # clean up data
    final_results = dict(sorted(final_results.items()))
    # filter false occurance within 1 sec, cause I know the loop is longer than 1 sec
    FPS = 30
    # final_results = dict(filter(lambda x: x[0]>=30, final_results.items()))
    # filter noise
    threshold = 30
    # final_results = dict(filter(lambda x: x[1]>=threshold, final_results.items()))

    x = list(final_results.keys())
    y = list(final_results.values())
    # print(x)
    # print(y)
    plt.plot(x, y)
    plt.title('Simple Line Plot')
    plt.xlabel('Period')
    plt.ylabel('Count')

    freq = dict(sorted(final_results.items(), key=lambda item: item[1]))
    print(freq)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to analysis the cycle, ouput a graph with occurrence against period")
    parser.add_argument("input", metavar= "HASH_JSON", type=str)
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"{args.input} does not exist, or not a file")
        exit()

    analysis(args.input)
