with open("data.txt") as f:
    instructions = f.readlines()


def instruction_match(s: str, instruction: str):
    if s.startswith(instruction):
        s = s.lstrip(instruction)
        return int(s.strip())


horizontal = 0
depth = 0
for instruction in instructions:
    if v := instruction_match(instruction, "forward"):
        horizontal += v
    elif v := instruction_match(instruction, "up"):
        depth -= v
    elif v := instruction_match(instruction, "down"):
        depth += v
    else:
        raise ValueError(f"Unexpected instruction: {instruction!r}")


print("Part 1 horizontal x depth = value")
print(f"       {horizontal:10d} x {depth:8d} = {horizontal * depth}")


horizontal = 0
depth = 0
aim = 0
for instruction in instructions:
    if v := instruction_match(instruction, "forward"):
        horizontal += v
        depth += aim * v
    elif v := instruction_match(instruction, "up"):
        aim -= v
    elif v := instruction_match(instruction, "down"):
        aim += v
    else:
        raise ValueError(f"Unexpected instruction: {instruction!r}")


print("Part 2 horizontal x depth = value")
print(f"       {horizontal:10d} x {depth:8d} = {horizontal * depth}")
