from argparse import ArgumentParser
import math
from pathlib import Path
import re

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    line = f.read().splitlines()[0]

m = re.search(r": x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", line)
x1 = int(m.group(1))
x2 = int(m.group(2))
y1 = int(m.group(3))
y2 = int(m.group(4))

print(x1, x2, y1, y2)

# Analytical solution for vx0: vx0 = -1/2 + sqrt(1/2 + 2*d) given that the distance >= landing time
min_vx0 = - 1/2 + math.sqrt(1/2 + 2 * x1)
max_vx0 = - 1/2 + math.sqrt(1/2 + 2 * x2)

min_vx0_int = math.ceil(min_vx0)
max_vx0_int = math.floor(max_vx0)
vx0 = list(range(min_vx0_int, max_vx0_int + 1))[0]
max_vy0 = vy0 = -min(y1, y2) - 1
print(f"Velocity vx0 range in [{min_vx0_int}, {max_vx0_int}]")
print(f"Part 1: Initial velocity: {vx0=}, {vy0=}")


def brute_force_landing_position(vx0, vy0):
    t = vy0 * 2 + 2
    vx = vx0
    vy = vy0
    x = 0
    y = 0
    for _ in range(t):
        x += vx
        y += vy
        if vx > 0:
            vx -= 1
        vy -= 1
    return x, y


x, y = brute_force_landing_position(vx0, vy0)
max_height = (vy0 + 1) * vy0 / 2

print(f"Landing position: {x}, {y}")
print(f"Part 1: {vx0, vy0=} => {max_height:.0f}\n")


def check_if_sticks_landing(vx0, vy0):
    x, y = 0, 0
    vx, vy = vx0, vy0
    while x < x2 and y > y1:
        x += vx
        y += vy
        vx = max(0, vx - 1)
        vy -= 1
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
    return False


shots = set()
for vx0 in range(1, x2+1):
    for vy0 in range(y1, max_vy0 + 1):
        if check_if_sticks_landing(vx0, vy0):
            shots.add((vx0, vy0))

print(f"Part 2: {len(shots)=}\n")
