from argparse import ArgumentParser
from pathlib import Path
import numpy as np
from scipy.signal import convolve2d

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

energy_levels0 = np.empty((10, 10), dtype=int)
with open(args.input_file) as f:
    for i, line in enumerate(f.readlines()):
        for j, c in enumerate(line.strip()):
            energy_levels0[i][j] = int(c)


def step(energy_levels):
    energy_levels = energy_levels.copy() + 1
    all_flashers = np.zeros_like(energy_levels, dtype=bool)
    while True:
        flashers = np.logical_and(energy_levels > 9, np.logical_not(all_flashers))
        all_flashers = np.logical_or(all_flashers, flashers)
        if np.count_nonzero(flashers) == 0:
            break
        energy_levels = energy_levels + convolve2d(flashers, np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]), mode="same")
        energy_levels[flashers] = 0
    energy_levels[all_flashers] = 0
    return np.count_nonzero(all_flashers), energy_levels


flash_count = 0
energy_levels = energy_levels0.copy()
for i in range(100):
    flashes, energy_levels = step(energy_levels)
    flash_count += flashes


i = 0
energy_levels = energy_levels0.copy()
while True:
    i += 1
    flashes, energy_levels = step(energy_levels)
    if np.all(energy_levels == 0):
        sync_index = i
        break


print(f"Part 1: {flash_count=}")
print(f"Part 2: {sync_index=}")
