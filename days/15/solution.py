from argparse import ArgumentParser
from pathlib import Path
import numpy as np

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.read().splitlines()


x_size = len(lines[0].strip())
y_size = len(lines)
risks = np.zeros((y_size, x_size))
for i, line in enumerate(lines):
    for j in range(x_size):
        risks[i, j] = int(line[j])

total_risks = np.zeros_like(risks)
total_risks[:] = float('inf')
last_x = np.zeros_like(risks, dtype=int)
last_y = np.zeros_like(risks, dtype=int)
visited = np.zeros_like(risks, dtype=bool)
exhausted = np.zeros_like(risks, dtype=bool)

visited[0, 0] = True
total_risks[0, 0] = 0

while not np.alltrue(exhausted):
    starting_points = np.where(np.logical_and(visited, np.logical_not(exhausted)))
    values = total_risks[starting_points]
    start_y, start_x, value = min(zip(starting_points[0], starting_points[1], values), key=lambda k: k[2])
    starting_point = np.array([start_y, start_x])

    # Left
    for y, x in (starting_point + [0, -1], starting_point + [1, 0], starting_point + [0, 1], starting_point + [-1, 0]):
        if not (0 <= x <= x_size - 1) or not (0 <= y <= y_size - 1):
            continue
        total_risk = risks[y, x] + total_risks[start_y, start_x]
        if total_risk < total_risks[y, x]:
            total_risks[y, x] = total_risk
            visited[y, x] = True
    exhausted[start_y, start_x] = True

total_risk = total_risks[y_size - 1, x_size - 1]

print(f"Part 1: {total_risk:.0f}\n")
print(f"Part 2: {0}\n")
