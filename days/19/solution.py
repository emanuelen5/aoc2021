from argparse import ArgumentParser
from pathlib import Path
from scanning import Scanning


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
    args = parser.parse_args()

    scannings = Scanning.read_file(args.input_file)

    print(f"Part 1: {0}\n")
    print(f"Part 2: {0}\n")
