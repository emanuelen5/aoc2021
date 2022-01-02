from argparse import ArgumentParser
import copy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

op_t = Union[list, int]
remainder_t = Union[int, None]

with open(args.input_file) as f:
    lines = f.read().splitlines()


@dataclass
class Snailnumber:
    left: Union["Snailnumber", int]
    right: Union["Snailnumber", None] = None
    parent: Union["Snailnumber", None] = field(repr=False, default=None)

    def is_leaf(self) -> bool:
        return isinstance(self.left, int)

    def as_list(self) -> Union[list, int]:
        if self.is_leaf():
            return self.left
        return [self.left.as_list(), self.right.as_list()]

    def __add__(self, other: "Snailnumber") -> "Snailnumber":
        if isinstance(other, list) or isinstance(other, int):
            other = Snailnumber.from_list(other)
        node = copy.deepcopy(self._join(other))
        to_reduce = True
        while to_reduce:
            exploded = node.explode()
            if exploded:
                continue
            node, splitted = node.split()
            if splitted:
                continue
            to_reduce = False
        return node

    def _join(self, rh: "Snailnumber") -> "Snailnumber":
        return Snailnumber.from_list([self.as_list(), rh.as_list()])

    def explode(self, depth: int = 0) -> bool:
        if isinstance(self.left, int):
            return False
        if depth >= 4:
            if not self.left.is_leaf() or not self.right.is_leaf():
                raise ValueError(f"Both left and right needs to be leafs. Got {self.left=} and {self.right=}.")
            self._send_left(self.left.left)
            self._send_right(self.right.left)
            self.left = 0
            self.right = None
            return True
        return self.left.explode(depth + 1) or self.right.explode(depth + 1)

    def _send_left(self, value: int):
        if self.parent is None:
            return
        # Go up until at parent with a left
        node = self
        while True:
            if not node.parent:
                return
            if id(node) == id(node.parent.right):
                node = node.parent
                break
            node = node.parent
        node = node.left
        while not node.is_leaf():
            node = node.right
        node.left += value

    def _send_right(self, value: int):
        if self.parent is None:
            return
        # Go up until at parent with a right
        node = self
        while True:
            if not node.parent:
                return
            if id(node) == id(node.parent.left):
                node = node.parent
                break
            node = node.parent
        node = node.right
        while not node.is_leaf():
            node = node.left
        node.left += value

    def split(self) -> tuple["Snailnumber", bool]:
        if self.is_leaf() and self.left >= 10:
            left_value = self.left // 2
            right_value = (self.left + 1) // 2
            self.left = Snailnumber(left_value, parent=self)
            self.right = Snailnumber(right_value, parent=self)
            return self, True
        elif self.is_leaf():
            return self, False

        left_node, splitted = self.left.split()
        if splitted:
            self.left = left_node
            return self, True
        right_node, splitted = self.right.split()
        if splitted:
            self.right = right_node
            return self, True
        return self, False

    def calc_magnitude(self) -> int:
        if isinstance(self.left, int):
            return self.left
        return self.left.calc_magnitude() * 3 + self.right.calc_magnitude() * 2

    @classmethod
    def from_list(cls, l: op_t, parent: "Snailnumber" = None):
        if isinstance(l, int):
            return cls(l, parent=parent)
        self = cls(cls.from_list(l[0]), cls.from_list(l[1]), parent=parent)
        self.left.parent = self
        self.right.parent = self
        return self

    def __repr__(self):
        return f"<{self.as_list()}>"


print(f"Part 1: {0}\n")
print(f"Part 2: {0}\n")
