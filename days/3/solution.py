import numpy as np
from pathlib import Path


with open(Path(__file__).parent / "data.txt") as f:
    lines = [line.strip() for line in f.readlines()]

bit_count = len(lines[0])
bit_patterns = np.zeros((len(lines), bit_count), dtype=np.uint8)
for i, line in enumerate(lines):
    for j, bit in enumerate(line):
        bit_patterns[i][j] = bit == "1"

bit_averages = bit_patterns.mean(axis=0).round().astype(np.uint8)

inverted_bit_averages = 1 - bit_averages
print(f"bit averages: {bit_averages}")
print(f"inverted    : {inverted_bit_averages}")


def array2bin(arr: np.ndarray) -> int:
    return int("".join(str(i) for i in arr), 2)


gamma = array2bin(bit_averages)
epsilon = array2bin(inverted_bit_averages)

print("Part 1 gamma x epsilon = power")
print(f"       {gamma} x {epsilon} = {gamma * epsilon}")
