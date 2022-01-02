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
class Node:
    left: Union["Node", int]
    right: Union["Node", None] = None
    parent: Union["Node", None] = field(repr=False, default=None)

    def is_leaf(self) -> bool:
        return isinstance(self.left, int)

    def as_list(self) -> Union[list, int]:
        if self.is_leaf():
            return self.left
        return [self.left.as_list(), self.right.as_list()]

    def add(self, rh: "Node") -> "Node":
        node = copy.deepcopy(self._join(rh))
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

    def _join(self, rh: "Node") -> "Node":
        return Node.from_list([self.as_list(), rh.as_list()])

    def needs_explode(self, depth: int = 0) -> bool:
        if depth >= 4:
            return True
        if isinstance(self.left, int):
            return False
        return self.left.needs_explode(depth + 1) or self.right.needs_explode(depth + 1)

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

    def split(self) -> tuple["Node", bool]:
        if self.is_leaf() and self.left >= 10:
            left_value = self.left // 2
            right_value = (self.left + 1) // 2
            self.left = Node(left_value, parent=self)
            self.right = Node(right_value, parent=self)
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

    def needs_split(self) -> bool:
        if isinstance(self.left, int):
            return self.left > 9
        return self.left.needs_split() or self.right.needs_split()

    def calc_magnitude(self) -> int:
        if isinstance(self.left, int):
            return self.left
        return self.left.calc_magnitude() * 3 + self.right.calc_magnitude() * 2

    @classmethod
    def from_list(cls, l: op_t, parent: "Node" = None):
        if isinstance(l, int):
            return cls(l, parent=parent)
        self = cls(cls.from_list(l[0]), cls.from_list(l[1]), parent=parent)
        self.left.parent = self
        self.right.parent = self
        return self

    def __repr__(self):
        return f"<{self.as_list()}>"


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


print(f"Part 1: {0}\n")
print(f"Part 2: {0}\n")
