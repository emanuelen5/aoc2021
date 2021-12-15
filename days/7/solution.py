from argparse import ArgumentParser
from pathlib import Path
import numpy as np

parser = ArgumentParser()
parser.add_argument("--input_file", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

crabs = np.loadtxt(args.input_file, delimiter=",").astype(int)
optimal_position = np.median(crabs)
total_fuel = np.sum(np.abs(crabs - optimal_position))
print(f"Part 1: Best position={int(optimal_position):<4} => fuel={int(total_fuel):9}")

best_fuel = float("inf")
best_fuel_pos = 0
for pos in range(np.min(crabs), np.max(crabs)+1):
    distances = np.abs(crabs - pos)
    fuel_cost = np.sum(distances * (distances + 1)) / 2
    if fuel_cost < best_fuel:
        best_fuel_pos = pos
        best_fuel = fuel_cost

print(f"Part 2: Best position={best_fuel_pos:<4} => fuel={int(best_fuel):9}")
