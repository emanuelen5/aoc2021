from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.read().splitlines()

mappings = []
for line in lines:
    mappings.append(line.split("-"))

nodes = set(m[0] for m in mappings).union(set(m[1] for m in mappings))

connections = {m: [] for m in nodes}
for mapping in mappings:
    connections[mapping[0]].append(mapping[1])
    connections[mapping[1]].append(mapping[0])

visits = {c: 0 for c in connections.keys()}


def explore_paths(from_node: str) -> int:
    if from_node == "end":
        return 1
    visits[from_node] += 1
    sum_ = 0
    for to_node in connections[from_node]:
        if to_node.upper() == to_node or visits[to_node] < 1:
            sum_ += explore_paths(to_node)
    visits[from_node] -= 1
    return sum_


paths = explore_paths("start")

print(f"Part 1: {paths}")
