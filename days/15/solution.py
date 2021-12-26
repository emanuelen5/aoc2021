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

for end_x, end_y in ((width - 1, height - 1), (width*5 - 1, height*5 - 1)):
    risks = np.zeros((height * 5, width * 5))
    for ii in range(5):
        for jj in range(5):
            for i, line in enumerate(lines):
                for j in range(width):
                    risks[i + ii * height, j + jj * width] = ((int(line[j]) + ii + jj - 1) % 9) + 1

    exhausted = {(0, 0)}
    to_visit = [(0, 0, 0)]

    i = 0
    to_visit_lookup = {(0, 0): 0}
    while to_visit:
        risk, y, x = heappop(to_visit)
        to_visit_lookup.pop((y, x), None)
        if x == end_x and y == end_y:
            print(f"Total risk: {risk:.0f}")
            break

        for y_, x_ in ([y, x-1], [y+1, x], [y, x+1], [y-1, x]):
            if (y_, x_) not in exhausted and (0 <= x_ <= end_x) and (0 <= y_ <= end_y):
                total_risk = risks[y_, x_] + risk
                if total_risk < to_visit_lookup.get((y_, x_), float('inf')):
                    heappush(to_visit, (total_risk, y_, x_))
                    to_visit_lookup[(y_, x_)] = total_risk
                exhausted.add((y, x))
        i += 1
