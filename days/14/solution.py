from argparse import ArgumentParser
from pathlib import Path
import time

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


def gen_characters(template, rules: dict[str, dict[str, str]]):
    yield template[0]
    for last_c, curr_c in zip(template[:-1], template[1:]):
        try:
            yield rules[last_c][curr_c]
        except KeyError:
            pass
        yield curr_c


def polymerize(template: str, rules: dict[str, dict[str, str]]) -> str:
    buffer = bytearray(2*len(template))
    i = 0
    for i, c in enumerate(gen_characters(template, rules)):
        buffer[i] = ord(c)
    return buffer[:i].decode("ascii")


for i in range(1, 19):
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
