from argparse import ArgumentParser
from pathlib import Path
import numpy as np

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.readlines()

height_map = np.zeros((len(lines), len(lines[0].strip())), dtype=np.int8)
for i, line in enumerate(lines):
    for j, s in enumerate(line.strip()):
        height_map[i][j] = int(s)

height_map = np.pad(height_map, pad_width=1, constant_values=10)

# Find low points
height, width = (i-2 for i in height_map.shape)
neighbors_offset = np.array([[-1, 0], [0, -1], [0, 1], [1, 0]])
local_minima = np.zeros_like(height_map, dtype=bool)
for i in range(1, height+1):
    for j in range(1, width+1):
        neighbors = neighbors_offset.copy()
        neighbors[:, 0] += i
        neighbors[:, 1] += j
        comparisons = height_map[i, j] < height_map[neighbors[:,0], neighbors[:,1]]
        local_minima[i, j] = np.all(comparisons)

risk = np.sum(height_map[local_minima] + 1)

print(f"Height map: \n{height_map}")
print(f"Local minima: {local_minima}")
print(f"Part 1: {risk=}")
