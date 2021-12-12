from argparse import ArgumentParser
from pathlib import Path
import numpy as np

parser = ArgumentParser()
parser.add_argument("--input_file", default=Path(__file__).parent / "data.txt")
parser.add_argument("--generations", default=80, help="Generation to simulate for")
args = parser.parse_args()

fishes = np.loadtxt(args.input_file, dtype=np.int8, delimiter=",")
print(f"{fishes.size:6d}: {fishes}")

for i_gen in range(args.generations):
    fishes = fishes - 1
    spawners = fishes < 0
    spawn_count = np.count_nonzero(spawners)
    fishes[spawners] = 6
    fishes = np.hstack((fishes, np.full((spawn_count,), 8)))
    print(f"{fishes.size:6d}")
