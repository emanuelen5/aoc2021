from argparse import ArgumentParser
from pathlib import Path
import re

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.read().splitlines()

polymer = lines[0]
insertion_rules = []
for line in lines[2:]:
    pair, insert = line.split(" -> ")
    insertion_rules.append((pair, insert))

print(f"{polymer=}")
print(f"{insertion_rules=}")


def polymerize(template: str, rules: list[tuple[str, str]]) -> str:
    insertions = []  # Where to insert each letter
    for pair, insert in rules:
        for match in re.finditer(rf"(?={pair})", template):
            insertions.append((match.start() + 1, insert))

    for start, insert in sorted(insertions, key=lambda i: i[0], reverse=True):
        template = template[:start] + insert + template[start:]
    return template


for i in range(10):
    polymer = polymerize(polymer, insertion_rules)
    print(f"{len(polymer):4}, {polymer=}")

letter_counts = {c: polymer.count(c) for c in set(polymer)}

print(f"{letter_counts=}")

print(f"Part 1: {max(letter_counts.values()) - min(letter_counts.values())}\n")
print(f"Part 2: ")
