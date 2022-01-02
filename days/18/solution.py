from argparse import ArgumentParser
import json
from pathlib import Path
import numpy as np
from snailnumber import Snailnumber

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lists = [json.loads(line) for line in f.read().splitlines()]


def add_from_list(lists):
    sn = Snailnumber.from_list(lists[0])
    for list_ in lists[1:]:
        sn = sn + list_
    return sn


print(f"Part 1: {add_from_list(lists).calc_magnitude()}\n")


def addition_combinations(lists):
    combination_matrix = np.zeros((len(lists), len(lists)), dtype=int)
    for i, list1 in enumerate(lists):
        for j, list2 in enumerate(lists[i+1:]):
            combination_matrix[i, j+i+1] = (Snailnumber.from_list(list1) + Snailnumber.from_list(list2)).calc_magnitude()
    return combination_matrix


np.set_printoptions(threshold=np.inf)
res = addition_combinations(lists)

print(f"Part 2: {np.amax(res, axis=None)}\n")
