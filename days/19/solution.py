from argparse import ArgumentParser
from pathlib import Path
from scanning import Scanning, _find_jumps_to_scanner


def find_unique_nodes(scannings: Scanning, result: list[tuple[int, int, tuple[int, int, int], tuple[int, int, int]]]) -> int:
    all_mappings = set(tuple(sorted((scanner1, scanner2))) for scanner1, scanner2, *_ in result)
    for i in range(len(scannings)):
        jumps = _find_jumps_to_scanner(all_mappings, i)
        print(jumps)
    return 0


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

    print(f"Part 1: {find_unique_nodes(scannings, results)}\n")
    print(f"Part 2: {0}\n")
