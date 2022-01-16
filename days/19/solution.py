from argparse import ArgumentParser
from pathlib import Path
from scanning import Scanning, _find_jumps_to_scanner
import numpy as np


def find_jumps(scannings: Scanning, result: list[tuple[int, int, tuple[int, int, int], tuple[int, int, int]]]) -> int:
    all_mappings = set(tuple(sorted((scanner1, scanner2))) for scanner1, scanner2, *_ in result)
    jumps = dict()
    for i in range(len(scannings)):
        jumps[i] = _find_jumps_to_scanner(all_mappings, i)
    return jumps


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
    args = parser.parse_args()

    scannings = Scanning.read_file(args.input_file)
    results = []
    for i, scanning1 in enumerate(scannings):
        print(i)
        for j, scanning2 in enumerate(scannings):
            if i <= j:
                continue
            corr_count, corr_angle, corr_offset = scanning1.find_cross_correlation(scanning2, threshold=12)
            if corr_count >= 12:
                results.append((i, j, corr_count, corr_angle, corr_offset))

    jump_map = find_jumps(scannings, results)
    # Nodes' position relative to origin
    nodes = set()

    for to, jumps in jump_map.items():
        for jump in jumps[1:]:
            # find corresponding in results
            left, right, _, angles, offset = [v for v in results if jump in v[:2]][0]
            angles = np.array(angles)
            offset = np.array(offset)
            # Invert transform if point of origin was the other one
            if right == to:
                angles = -angles
                offset = -offset

    print(f"Part 1: {find_jumps(scannings, results)}\n")
    print(f"Part 2: {0}\n")
