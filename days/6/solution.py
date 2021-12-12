from argparse import ArgumentParser
from pathlib import Path
import numpy as np

parser = ArgumentParser()
parser.add_argument("--input_file", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

fishes = np.loadtxt(args.input_file, dtype=np.int8, delimiter=",")
print(f"{fishes.size}: {fishes}")
fish_bins, _ = np.histogram(fishes, bins=range(10))
fish_bins = fish_bins.astype(np.uint64)

for i_gen in range(1, 256 + 1):
    new_fishes = fish_bins[0]
    fish_bins[0:8] = fish_bins[1:9]
    fish_bins[8] = new_fishes
    fish_bins[6] += new_fishes
    print(f"{i_gen}: {fish_bins.sum()}: {fish_bins}")
    if i_gen == 80:
        print(f"Part 1: {fish_bins.sum()}")
    elif i_gen == 256:
        print(f"Part 2: {fish_bins.sum()}")
