from argparse import ArgumentParser
from pathlib import Path
from scanning import Scanning


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
            corr_count, corr_angle, corr_offset = scanning1.find_cross_correlation(scanning2)
            if corr_count >= 12:
                results.append((i, j, corr_count, corr_angle, corr_offset))

    print(f"Part 1: {0}\n")
    print(f"Part 2: {0}\n")
