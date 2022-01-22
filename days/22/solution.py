from argparse import ArgumentParser
from pathlib import Path
import re

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.read().splitlines()


instructions = []
re_pattern = re.compile(r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")
for line in lines:
    m = re_pattern.match(line)
    on = m.group(1) == "on"
    nums = tuple(int(m.group(i)) for i in range(2, 8))
    x = nums[0:2]
    y = nums[2:4]
    z = nums[4:6]
    instructions.append((on, x, y, z))


lighted_cube_t = set[tuple[int, int, int]]
lighted_cubes = set()

def turn_on(lighted_cubes: lighted_cube_t, xs, ys, zs) -> lighted_cube_t:
    for x in range(max(-50, xs[0]), min(xs[1], 50)+1):
        for y in range(max(-50, ys[0]), min(ys[1], 50)+1):
            for z in range(max(-50, zs[0]), min(zs[1], 50)+1):
                lighted_cubes.add((x, y, z))
    return lighted_cubes

def turn_off(lighted_cubes: lighted_cube_t, xs, ys, zs) -> lighted_cube_t:
    for x, y, z in lighted_cubes.copy():
        if xs[0] <= x <= xs[1] and \
           ys[0] <= y <= ys[1] and \
           zs[0] <= z <= zs[1]:
            lighted_cubes.remove((x, y, z))
    return lighted_cubes


for i, (on, xs, ys, zs) in enumerate(instructions):
    print(f"{i}/{len(instructions)}")
    if on:
        lighted_cubes = turn_on(lighted_cubes, xs, ys, zs)
    else:
        lighted_cubes = turn_off(lighted_cubes, xs, ys, zs)


print(f"Part 1: {len(lighted_cubes)}\n")
print(f"Part 2: {0}\n")
