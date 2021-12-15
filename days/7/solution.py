from argparse import ArgumentParser
from pathlib import Path
import numpy as np

parser = ArgumentParser()
parser.add_argument("--input_file", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

crabs = np.loadtxt(args.input_file, delimiter=",")
optimal_position = np.median(crabs)
total_fuel = np.sum(np.abs(crabs - optimal_position))
print(f"Part 1: {total_fuel}")
