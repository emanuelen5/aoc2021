from dataclasses import dataclass
from pathlib import Path
import numpy as np
import re

re_pattern = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")


@dataclass
class Line:
    x1: int
    y1: int
    x2: int
    y2: int

    def is_horizontal(self) -> bool:
        return self.y1 == self.y2

    def is_vertical(self) -> bool:
        return self.x1 == self.x2

    def is_diagonal_down(self) -> bool:
        return (self.x2 - self.x1) == (self.y2 - self.y1)

    def is_diagonal_up(self) -> bool:
        return (self.x2 - self.x1) == -(self.y2 - self.y1)

    @classmethod
    def from_line(cls, line: str):
        m = re_pattern.match(line)
        return cls(
            int(m.group(1)),
            int(m.group(2)),
            int(m.group(3)),
            int(m.group(4)),
        )

    def __repr__(self):
        return f"<Line ({self.x1},{self.y1}) -> ({self.x2},{self.y2})>"


with open(Path(__file__).parent / "data.txt") as f:
    lines = [Line.from_line(line) for line in f.readlines()]

grid1 = np.zeros((1000, 1000), np.uint16)
grid2 = np.zeros((1000, 1000), np.uint16)
for line in lines:
    min_y = min(line.y1, line.y2)
    max_y = max(line.y1, line.y2)
    min_x = min(line.x1, line.x2)
    max_x = max(line.x1, line.x2)
    if line.is_vertical():
        grid1[min_y:max_y + 1, line.x1] += 1
        grid2[min_y:max_y + 1, line.x1] += 1
    elif line.is_horizontal():
        grid1[line.y1, min_x:max_x + 1] += 1
        grid2[line.y1, min_x:max_x + 1] += 1
    elif line.is_diagonal_down():
        for x, y in zip(range(min_x, max_x + 1), range(min_y, max_y + 1)):
            grid2[y, x] += 1
    elif line.is_diagonal_up():
        for x, y in zip(range(min_x, max_x + 1), range(max_y, min_y - 1, -1)):
            grid2[y, x] += 1
    else:
        print(f"Unhandled line: {line}")

atleast_2_part1 = np.count_nonzero(grid1 >= 2)
atleast_2_part2 = np.count_nonzero(grid2 >= 2)
print(f"Part 1: At least two overlaps {atleast_2_part1}")
print(f"Part 2: At least two overlaps {atleast_2_part2}")
