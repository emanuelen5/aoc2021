from argparse import ArgumentParser
from pathlib import Path
import numpy as np

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = [l.strip() for l in f.readlines()]

parens_equivalents = {'(': ')', '{': '}', '[': ']', '<': '>'}
parens_score = {')': 3, '}': 1197, ']': 57, '>': 25137}
completion_score = {')': 1, ']': 2, '}': 3, '>': 4}

line_uncomplete_scores = []
line_completion_scores = []
for line in lines:
    parens_stack = []
    for char in line:
        if char in parens_equivalents.keys():
            parens_stack.append(char)
        elif char == parens_equivalents[parens_stack[-1]]:
            parens_stack.pop()
        else:
            line_uncomplete_scores.append(parens_score[char])
            break
    else:
        missing_parens = [parens_equivalents[p] for p in reversed(parens_stack)]
        score = 0
        for p in missing_parens:
            score *= 5
            score += completion_score[p]
        line_completion_scores.append(score)
        print(score)

print(f"Part 1: {sum(line_uncomplete_scores)=}")
print(f"Part 2: {int(np.median(line_completion_scores))=}")
