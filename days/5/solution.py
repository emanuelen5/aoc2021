from dataclasses import dataclass
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

    @classmethod
    def from_line(cls, line: str):
        m = re_pattern.match(line)
        return cls(
            int(m.group(1)),
            int(m.group(2)),
            int(m.group(3)),
            int(m.group(4)),
        )


with open("data.txt") as f:
    lines = [Line.from_line(line) for line in f.readlines()]

grid = np.zeros((1000, 1000))
for line in lines:
    if line.is_vertical():
        min_y = min(line.y1, line.y2)
        max_y = max(line.y1, line.y2)
        grid[min_y:max_y + 1, line.x1] += 1
    elif line.is_horizontal():
        min_x = min(line.x1, line.x2)
        max_x = max(line.x1, line.x2)
        grid[line.y1, min_x:max_x + 1] += 1

atleast_2 = np.count_nonzero(grid >= 2)
print(f"Part 1: At least two overlaps {atleast_2}")
