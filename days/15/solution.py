from argparse import ArgumentParser
from pathlib import Path
from heapq import heappop, heappush
import numpy as np

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.read().splitlines()


width = len(lines[0].strip())
height = len(lines)
risks = np.zeros((height * 5, width * 5))
for ii in range(5):
    for jj in range(5):
        for i, line in enumerate(lines):
            for j in range(width):
                risks[i + ii * height, j + jj * width] = ((int(line[j]) + ii + jj - 1) % 9) + 1

total_risks = np.zeros_like(risks)
total_risks[:] = float('inf')
exhausted = {(0, 0)}
to_visit = [(0, 0, 0)]

total_risks[0, 0] = 0

while to_visit:
    risk, y, x = heappop(to_visit)

    for y_, x_ in ([y, x-1], [y+1, x], [y, x+1], [y-1, x]):
        if (y_, x_) not in exhausted and (0 <= x_ <= width * 5 - 1) and (0 <= y_ <= height * 5 - 1):
            total_risk = risks[y_, x_] + risk
            if total_risk < total_risks[y_, x_]:
                total_risks[y_, x_] = total_risk
            heappush(to_visit, (total_risk, y_, x_))
            exhausted.add((y, x))

print(f"Part 1: {total_risks[height - 1, width - 1]:.0f}\n")
print(f"Part 2: {total_risks[height * 5 - 1, width * 5 - 1]:.0f}\n")
