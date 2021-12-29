from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Union

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

op_t = Union[list, int]
remainder_t = Union[int, None]

with open(args.input_file) as f:
    lines = f.read().splitlines()


def needs_explode(l: op_t, depth: int = 0) -> bool:
    if depth >= 4:
        return True
    if isinstance(l, int):
        return False
    return needs_explode(l[0], depth+1) or needs_explode(l[1], depth+1)


def needs_split(l: op_t) -> bool:
    if isinstance(l, int):
        return l > 9
    return needs_split(l[0]) or needs_split(l[1])


def calc_magnitude(l: op_t) -> int:
    if isinstance(l, int):
        return l
    return calc_magnitude(l[0]) * 3 + calc_magnitude(l[1]) * 2


@dataclass
class Node:
    left: Union["Node", int]
    right: Union["Node", None] = None
    parent: Union["Node", None] = None

    def add_right(self, value: int):
        pass

    def add_left(self, value: int):
        pass

    def is_leaf(self) -> bool:
        return isinstance(self.left, int)

    def as_list(self) -> list:
        if self.is_leaf():
            return self.left
        return [self.left.as_list(), self.right.as_list()]

    @classmethod
    def from_list(cls, l: op_t, parent: "Node" = None):
        if isinstance(l, int):
            return cls(l)
        return cls(cls.from_list(l[0]), cls.from_list(l[1]), l)


def _explode(l: op_t, depth: int = 0, parent: op_t = None) -> tuple[op_t, remainder_t, remainder_t, bool]:
    if isinstance(l, int):
        return l, None, None, False
    if depth == 4:
        return 0, l[0], l[1], True
    l_new, rem_l, rem_r, done = _explode(l[0], depth+1, l)
    l[0] = l_new
    if not done:
        r_new, rem_l, rem_r, done = _explode(l[1], depth+1, l)
    return l_new, None, None, done


def explode(l: list) -> list:
    return _explode(l)


def split(l: list) -> list:
    return l


def add(l1: list, l2: list) -> list:
    return [l1, l2]


print(f"Part 1: {0}\n")
print(f"Part 2: {0}\n")
