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
    has_won: bool = False
    final_score: int = field(init=False, default=None)

    def draw(self, num: int):
        self.checked[self.board == num] = True
        self.has_won = self.has_bingo()
        if self.has_won:
            self.final_score = self._get_score(num)

    def has_bingo(self) -> bool:
        for i in range(5):
            if all(self.checked[i, :]) or all(self.checked[:, i]):
                return True
        # Diagonal 1?
        # Diagonal 2?

    def _get_score(self, last_draw: int) -> int:
        unmarked = self.board[np.logical_not(self.checked)]
        return last_draw * np.sum(unmarked)


boards = []
re_pattern = re.compile(" +")
for bingo_lines in chunks(lines[1:], 6):
    values = [[int(l) for l in re_pattern.split(line.strip())] for line in bingo_lines[1:]]
    board = BingoBoard(np.array(values))
    boards.append(board)

first_winner_idx, first_winner = None, None
last_winner_idx, last_winner = None, None
for draw in draws:
    for i, board in enumerate(list(boards)):
        if not board.has_won:
            board.draw(draw)
            if board.has_won:
                last_winner_idx = i
                last_winner = board
        if first_winner is None and board.has_won:
            first_winner_idx = i
            first_winner = board

print(f"First bingo was for board {first_winner_idx}!:)")
print(f"\t{first_winner!r}")
print(f"Score: {first_winner.final_score}")

print(f"Last bingo was for board {last_winner_idx}!:)")
print(f"\t{last_winner!r}")
print(f"Score: {last_winner.final_score}")
