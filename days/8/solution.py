from argparse import ArgumentParser
from pathlib import Path
import numpy as np

parser = ArgumentParser()
parser.add_argument("--input_file", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.readlines()

number_sum = 0
for line in lines:
    line = line[line.index("|")+1:].strip()
    values = line.split(" ")
    digits = [s for s in values if len(s) in (2, 3, 4, 7)]
    number_sum += len(digits)

print(f"Part 1: {number_sum}")
