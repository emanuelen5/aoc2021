with open("data.txt") as f:
    depths = [int(line) for line in f.readlines()]

increasing_depths = 0

last_depth = depths[0]
for depth in depths[1:]:
    if depth > last_depth:
        increasing_depths += 1
    last_depth = depth

print(f"Part 1 increasing depths: {increasing_depths}")

increasing_depths = 0
last_depth = sum(depths[0:3])
for (d1, d2, d3) in zip(depths[:-2], depths[1:-1], depths[2:]):
    sum_depth = sum([d1, d2, d3])
    if sum_depth > last_depth:
        increasing_depths += 1
    last_depth = sum_depth

print(f"Part 2 increasing mean depths: {increasing_depths}")
