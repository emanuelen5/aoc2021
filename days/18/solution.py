from argparse import ArgumentParser
import json
from pathlib import Path
from snailnumber import Snailnumber

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lists = [json.loads(line) for line in f.read().splitlines()]

sn = Snailnumber.from_list(lists[0])
for list_ in lists:
    sn = sn + list_


print(f"Part 1: {sn.calc_magnitude()}\n")
print(f"Part 2: {0}\n")
