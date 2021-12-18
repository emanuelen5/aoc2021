from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = [l.strip() for l in f.readlines()]

parens_equivalents = {'(': ')', '{': '}', '[': ']', '<': '>'}
parens_score = {')': 3, '}': 1197, ']': 57, '>': 25137}

line_uncomplete_score = []
for line in lines:
    parens_stack = []
    for char in line:
        if char in parens_equivalents.keys():
            parens_stack.append(char)
        elif char == parens_equivalents[parens_stack[-1]]:
            parens_stack.pop()
        else:
            line_uncomplete_score.append(parens_score[char])
            break

print(f"Part 1: {sum(line_uncomplete_score)=}")
