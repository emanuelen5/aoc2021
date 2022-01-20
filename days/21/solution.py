from argparse import ArgumentParser
from math import perm
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.read().splitlines()

start_a = int(lines[0].split(" ")[-1])
start_b = int(lines[1].split(" ")[-1])

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


def play_game(start_a: int, start_b: int) -> tuple[int, int]:
    player_a_pos = start_a
    player_b_pos = start_b
    sum1 = sum2 = 0
    dice = DeterministicDice()
    dicer = dice.generate_throws()
    while True:
        steps = sum([d for _, d in zip(range(3), dicer)])
        player_a_pos = (player_a_pos + steps - 1) % 10 + 1
        sum1 += player_a_pos
        if sum1 >= 1000:
            return dice.throws, min(sum1, sum2)

        steps = sum([d for _, d in zip(range(3), dicer)])
        player_b_pos = (player_b_pos + steps - 1) % 10 + 1
        sum2 += player_b_pos
        if sum2 >= 1000:
            return dice.throws, min(sum1, sum2)

throws, min_score = play_game(start_a, start_b)

print(f"Part 1: {throws * min_score}\n")

# Number of permutations for getting different sums with quantum dice
quantum_sum_permutations = dict()
for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            sum_ = i + j + k
            quantum_sum_permutations[sum_] = quantum_sum_permutations.get(sum_, 0) + 1

def calc_quantum_win_counts_lookup(
    pos: int, 
    rounds: int = 0, 
    score: int = 0, 
    permutations: int = 1, 
    win_lookup: dict[int, int] = None
) -> dict[int, int]:
    """ Calculates a lookup table of the number of permutations (universes) in which one will reach the goal within a given number of rounds. """
    if win_lookup is None:
        win_lookup = dict()
    if score >= 21:
        win_lookup[rounds] = win_lookup.get(rounds, 0) + permutations
        return win_lookup
    for steps, steps_perms in quantum_sum_permutations.items():
        pos_next = (pos + steps - 1) % 10 + 1
        calc_quantum_win_counts_lookup(pos_next, rounds + 1, score + pos_next, permutations * steps_perms, win_lookup)
    return win_lookup

finishes_a = calc_quantum_win_counts_lookup(start_a)
finishes_b = calc_quantum_win_counts_lookup(start_b)

def calc_permutations_not_won_yet_lookup(wins: dict[int, int]) -> dict[int, int]:
    """ Calculate, for each round, how many permutations that have not yet won. """
    not_won_yet = dict()
    permutations_not_won_yet = 1
    for round in range(1, max(wins.keys()) + 1):
        permutations_not_won_yet *= 3**3  # The dice are rolled three times, with three sides for each round
        permutations_not_won_yet -= wins.get(round, 0)  # Remove the permutations that win at this round
        not_won_yet[round] = permutations_not_won_yet
    return not_won_yet


not_won_yet_lookup_a = calc_permutations_not_won_yet_lookup(finishes_a)
not_won_yet_lookup_b = calc_permutations_not_won_yet_lookup(finishes_b)

# 2 reaches 21 in less amount of rounds => 2 wins
# otherwise => 1 wins
wins_for_a = 0
wins_for_b = 0
for rounds in set(finishes_a.keys()) or set(finishes_b.keys()):
    wins_for_a += finishes_a.get(rounds, 0) * not_won_yet_lookup_b.get(rounds - 1, 0)
    wins_for_b += finishes_b.get(rounds, 0) * not_won_yet_lookup_a.get(rounds, 0)

print(f"Part 2: {max(wins_for_a, wins_for_b)} ({wins_for_a=} vs {wins_for_b=})\n")
