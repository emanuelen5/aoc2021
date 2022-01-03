from argparse import ArgumentParser
import numpy as np
from pathlib import Path
import re
from scanning import Scanning

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()


with open(args.input_file) as f:
    lines = f.read().splitlines()
lines = [line for line in lines if len(line)]


scan_pattern = re.compile(r"^--- scanner (\d+) ---$")
scanning_values = id_ = None
scannings = []
for line in lines:
    if m := scan_pattern.match(line):
        if scanning_values is not None:
            scanning_values = np.array(scanning_values)
            scanning = Scanning(scanning_values, id_)
            scannings.append(scanning)
        id_ = int(m.group(1))
        scanning_values = []
        continue
    scanning_values.append([int(v) for v in line.split(",")])

print(f"Part 1: {0}\n")
print(f"Part 2: {0}\n")
