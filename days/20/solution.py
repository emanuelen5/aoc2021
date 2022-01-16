from argparse import ArgumentParser
from pathlib import Path
import numpy as np
from scipy.signal import correlate2d

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.read().splitlines()

lookup = [1 if v == "#" else 0 for v in lines[0]]
kernel = [
    [256, 128,  64],
    [ 32,  16,   8],
    [  4,   2,   1],
]
image = np.array([[1 if v == "#" else 0 for v in line] for line in lines[2:]])
background_color = 0

def transform(img):
    global background_color
    values = correlate2d(img, kernel, mode='full', fillvalue=background_color)
    background_color = lookup[background_color]
    h, w = values.shape
    output = np.zeros_like(values)
    for i in range(h):
        for j in range(w):
            output[i, j] = lookup[values[i, j]]
    return output

print(f"Part 1: \n{np.count_nonzero(transform(transform(image)))}\n")
# 5565

print(f"Part 2: {0}\n")
