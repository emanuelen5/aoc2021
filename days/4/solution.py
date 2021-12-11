from dataclasses import dataclass, field
from typing import List
import re
import numpy as np

with open("data.txt") as f:
    lines = [line.strip() for line in f.readlines()]

draws = [int(i) for i in lines[0].split(",")]


def chunks(list_: List, size: int):
    for i in range(0, len(list_), size):
        yield list_[i:i + size]


@dataclass
class BingoBoard:
    board: np.ndarray
    checked: np.ndarray = field(init=False, default_factory=lambda: np.zeros((5,5), dtype=bool))

    def draw(self, num: int):
        self.checked[self.board == num] = True

    def has_bingo(self) -> bool:
        for i in range(5):
            if all(self.checked[i, :]) or all(self.checked[:, i]):
                return True
        # Diagonal 1?
        # Diagonal 2?

    def get_score(self, last_draw: int) -> int:
        unmarked = self.board[np.logical_not(self.checked)]
        return last_draw * np.sum(unmarked)


boards = []
re_pattern = re.compile(" +")
for bingo_lines in chunks(lines[1:], 6):
    values = [[int(l) for l in re_pattern.split(line.strip())] for line in bingo_lines[1:]]
    board = BingoBoard(np.array(values))
    boards.append(board)

bingo = False
for draw in draws:
    for i, board in enumerate(list(boards)):
        board.draw(draw)
        if board.has_bingo():
            bingo = True
            print(f"Bingo for board {i}!:)")
            print(f"\t{board!r}")
            print(f"Score: {board.get_score(draw)}")
    if bingo:
        break
