from argparse import ArgumentParser
from pathlib import Path
from functools import cache

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.read().splitlines()

polymer = lines[0]
insertion_rules = dict()
for line in lines[2:]:
    pair, insert = line.split(" -> ")
    if pair[0] not in insertion_rules:
        insertion_rules[pair[0]] = dict()
    insertion_rules[pair[0]][pair[1]] = insert

print(f"{polymer=}")
print(f"{insertion_rules=}")


def increment_letter(dict_, a):
    dict_[a] = dict_.get(a, 0) + 1


def merge_letter_counts(a, b) -> dict[str, int]:
    merged = dict()
    all_letters = set(a.keys()).union(set(b.keys()))
    for l in all_letters:
        merged[l] = a.get(l, 0) + b.get(l, 0)
    return merged


@cache
def _polymerize_letter_count(a, b, height: int) -> dict[str, int]:
    letter_counts = dict()
    if height == 0:
        return letter_counts

    try:
        c = insertion_rules[a][b]
        letter_counts = merge_letter_counts(
            _polymerize_letter_count(a, c, height - 1),
            _polymerize_letter_count(c, b, height - 1)
        )
        increment_letter(letter_counts, c)
    except KeyError:
        pass

    return letter_counts


def polymerize_letter_count(template, depth: int) -> dict:
    letter_counts = dict()
    for l in template:
        increment_letter(letter_counts, l)
    for a, b in zip(template[:-1], template[1:]):
        letter_counts = merge_letter_counts(letter_counts, _polymerize_letter_count(a, b, depth))
    return letter_counts


letter_counts_10 = polymerize_letter_count(polymer, depth=10)
print(f"Part 1: {max(letter_counts_10.values()) - min(letter_counts_10.values())}\n")

letter_counts_40 = polymerize_letter_count(polymer, depth=40)
print(f"Part 2: {max(letter_counts_40.values()) - min(letter_counts_40.values())}\n")
