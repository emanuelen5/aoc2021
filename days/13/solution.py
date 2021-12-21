from argparse import ArgumentParser
from pathlib import Path
import re

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

dot_positions = set()
fold_instructions = []
with open(args.input_file) as f:
    while True:
        line = f.readline()
        if len(line.strip()) == 0:
            break
        dot_positions.add(tuple([int(l) for l in line.split(",")]))
    lines = f.read().splitlines()

fold_instructions = []
for line in lines:
    m = re.match(r"fold along ([xy])=(\d+)", line)
    fold_instructions.append((m.group(1), int(m.group(2))))


def do_fold(dots: set[tuple[int, ...]], dir_: str, pos: int) -> set[tuple[int, ...]]:
    folded_dots = set()
    for dot in dots:
        if dir_ == "x":
            dot = (dot[0] if dot[0] < pos else 2 * pos - dot[0], dot[1])
        elif dir_ == "y":
            dot = (dot[0], dot[1] if dot[1] < pos else 2 * pos - dot[1])
        folded_dots.add(dot)
    return folded_dots


def print_dots(dots: set[tuple[int, ...]]) -> None:
    max_x = max(dots, key=lambda k: k[0])[0]
    max_y = max(dots, key=lambda k: k[1])[1]
    for j in range(max_y + 1):
        for i in range(max_x + 1):
            if (i, j) in dots:
                print("# ", end="")
            else:
                print(". ", end="")
        print("")
    print()


fold_dir, fold_pos = fold_instructions[0]
dot_positions_first_fold = do_fold(dot_positions, fold_dir, fold_pos)
print(len(dot_positions_first_fold))

print(f"Part 1: \n")
print(f"Part 2: ")
