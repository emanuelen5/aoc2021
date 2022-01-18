from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.read().splitlines()


start1 = int(lines[0].split(" ")[-1])
start2 = int(lines[1].split(" ")[-1])

class DeterministicDice:
    def __init__(self) -> None:
        self.throws = 0

    def generate_throws(self):
        self.throws = 0
        i = 0
        while True:
            self.throws += 1
            i = i % 100 + 1
            yield i


def play_game(start1: int, start2: int) -> tuple[int, int]:
    player1_pos = start1
    player2_pos = start2
    sum1 = sum2 = 0
    dice = DeterministicDice()
    dicer = dice.generate_throws()
    while True:
        steps = sum([d for _, d in zip(range(3), dicer)])
        player1_pos = (player1_pos + steps - 1) % 10 + 1
        sum1 += player1_pos
        if sum1 >= 1000:
            return dice.throws, min(sum1, sum2)

        steps = sum([d for _, d in zip(range(3), dicer)])
        player2_pos = (player2_pos + steps - 1) % 10 + 1
        sum2 += player2_pos
        if sum2 >= 1000:
            return dice.throws, min(sum1, sum2)
        

throws, min_score = play_game(start1, start2)

print(f"Part 1: {throws * min_score}\n")


def find_wins(throws, score, win_lookup = {i+1:0 for i in range(21)}):
    if score >= 21:
        win_lookup[throws] += 1
        return win_lookup
    find_wins(throws+1, score+1, win_lookup)
    find_wins(throws+1, score+2, win_lookup)
    find_wins(throws+1, score+3, win_lookup)
    return win_lookup

wins = find_wins(0, 0)
print(wins)

print(f"Part 2: {0}\n")
