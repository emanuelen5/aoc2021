with open("data.txt") as f:
    instructions = f.readlines()


def instruction_match(s: str, instruction: str):
    if s.startswith(instruction):
        s = s.lstrip(instruction)
        return int(s.strip())


deltas = []
horizontal = 0
depth = 0
for instruction in instructions:
    if v := instruction_match(instruction, "forward"):
        deltas.append((v, 0))
        horizontal += v
    elif v := instruction_match(instruction, "up"):
        deltas.append((0, -v))
        depth -= v
    elif v := instruction_match(instruction, "down"):
        deltas.append((0, v))
        depth += v
    else:
        raise ValueError(f"Unexpected instruction: {instruction!r}")


print("Part 1 horizontal x depth = value")
print(f"       {horizontal:10d} x {depth:8d} = {horizontal * depth}")

# increasing_depths = 0
# last_depth = sum(depths[0:3])
# for (d1, d2, d3) in zip(depths[:-2], depths[1:-1], depths[2:]):
#     sum_depth = sum([d1, d2, d3])
#     if sum_depth > last_depth:
#         increasing_depths += 1
#     last_depth = sum_depth
#
# print(f"Part 2 increasing mean depths: {increasing_depths}")
