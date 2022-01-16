from argparse import ArgumentParser
from pathlib import Path
import numpy as np
from scipy.signal import convolve2d

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.read().splitlines()

lookup = [1 if v == "#" else 0 for v in lines[0]]
kernel = [
    [  1,   2,   4],
    [  8,  16,  32],
    [ 64, 128, 256],
]
image = np.array([[1 if v == "#" else 0 for v in line] for line in lines[2:]])

def transform(img):
    print(img.shape, np.count_nonzero(img), img)
    values = convolve2d(img, kernel, mode='full')
    h, w = values.shape
    output = np.zeros_like(values)
    for i in range(h):
        for j in range(w):
            output[i, j] = lookup[values[i, j]]
    return output

print(f"Part 1: \n{np.count_nonzero(transform(transform(image)))}\n")
# 5565

print(f"Part 2: {0}\n")
