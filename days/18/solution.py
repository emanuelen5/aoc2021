from argparse import ArgumentParser
from pathlib import Path
from typing import Union

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

optype = Union[list, int]

with open(args.input_file) as f:
    lines = f.read().splitlines()


def needs_explode(l: optype, depth: int = 0) -> bool:
    if depth >= 4:
        return True
    if isinstance(l, int):
        return False
    return needs_explode(l[0], depth+1) or needs_explode(l[1], depth+1)


def needs_split(l: optype) -> bool:
    if isinstance(l, int):
        return l > 9
    return needs_split(l[0]) or needs_split(l[1])


def calc_magnitude(l: optype) -> int:
    if isinstance(l, int):
        return l
    return calc_magnitude(l[0]) * 3 + calc_magnitude(l[1]) * 2


def explode(l: list) -> list:
    return l


def split(l: list) -> list:
    return l


def add(l1: list, l2: list) -> list:
    return [l1, l2]


print(f"Part 1: {0}\n")
print(f"Part 2: {0}\n")
