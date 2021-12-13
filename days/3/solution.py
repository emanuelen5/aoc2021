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


def bit_condition(vals: np.ndarray, type_: int):
    if type_ == 0:
        return 1 if vals.mean() >= 0.5 else 0
    return 0 if vals.mean() >= 0.5 else 1


bit_patterns2 = bit_patterns.copy()
for i in range(bit_count):
    search_pattern = bit_condition(bit_patterns2[:, i], 0)
    mask = bit_patterns2[:, i] == search_pattern
    bit_patterns2 = bit_patterns2[mask, :]
    if len(bit_patterns2) == 1:
        oxygen = array2bin(bit_patterns2[0])
        break
else:
    raise ValueError("Ran to end without finding answer")


bit_patterns2 = bit_patterns.copy()
for i in range(bit_count):
    search_pattern = bit_condition(bit_patterns2[:, i], 1)
    mask = bit_patterns2[:, i] == search_pattern
    bit_patterns2 = bit_patterns2[mask, :]
    if len(bit_patterns2) == 1:
        co2 = array2bin(bit_patterns2[0])
        break
else:
    raise ValueError("Ran to end without finding answer")


print("Part 2 oxygen x CO2 = life support")
print(f"       {oxygen} x {co2} = {oxygen * co2}")
