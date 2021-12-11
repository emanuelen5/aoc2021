from dataclasses import dataclass, field
from typing import List
import re

with open("data.txt") as f:
    lines = [line.strip() for line in f.readlines()]

draws = [int(i) for i in lines[0].split(",")]


def chunks(list_: List, size: int):
    for i in range(0, len(list_), size):
        yield list_[i:i + size]


@dataclass
class BingoBoard:
    board: List[List[int]]
    checked: List[List[bool]] = field(init=False, default_factory=lambda: [[False for _ in range(5)] for _ in range(5)])

    def draw(self, num: int):
        for r, row in enumerate(self.board):
            try:
                idx = row.index(num)
                self.checked[r][idx] = True
            except ValueError:
                pass

    def has_bingo(self) -> bool:
        # Horizontal
        for i in range(5):
            if all(self.checked[i]):
                return True
        # Vertical
        for i in range(5):
            vert = [self.checked[j][i] for j in range(5)]
            if all(vert):
                return True
        # Diagonal 1?
        # Diagonal 2?

    def get_score(self, last_num: int) -> int:



boards = []
re_pattern = re.compile(" +")
for bingo_lines in chunks(lines[1:], 6):
    values = [[int(l) for l in re_pattern.split(line.strip())] for line in bingo_lines[1:]]
    board = BingoBoard(values)
    boards.append(board)

bingo = False
for draw in draws:
    for i, board in enumerate(list(boards)):
        board.draw(draw)
        if board.has_bingo():
            bingo = True
            print(f"Bingo for board {i}! {board!r}")
    if bingo:
        break


