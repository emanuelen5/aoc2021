from argparse import ArgumentParser
from pathlib import Path
import re
import time

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


for i in range(1, 16):
    start_time = time.time()
    polymer = polymerize(polymer, insertion_rules)
    end_time = time.time()
    print(f"{i:2} => {len(polymer)=:4} (time = {end_time - start_time:.6f} s)")
    letter_counts = {c: polymer.count(c) for c in set(polymer)}
    print(f"\t{letter_counts=}")

    if i == 10:
        print(f"Part 1: {max(letter_counts.values()) - min(letter_counts.values())}\n")
    elif i == 40:
        print(f"Part 2: {max(letter_counts.values()) - min(letter_counts.values())}\n")
