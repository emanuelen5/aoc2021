with open("data.txt") as f:
    lines = [line.strip() for line in f.readlines()]


bit_count = len(lines[0])
bit_averages = []

gamma = 0
for bit_index in range(bit_count):
    bits = [int(line[bit_index]) for line in lines]
    common_value = max([0, 1], key = lambda k: bits.count(k))
    bit_averages.append(common_value)


inverted_bit_averages = [1-i for i in bit_averages]
print(f"bit averages: {bit_averages}")
print(f"inverted    : {inverted_bit_averages}")

gamma = int("".join(str(i) for i in bit_averages), 2)
epsilon = int("".join(str(i) for i in inverted_bit_averages), 2)

print("Part 1 gamma x epsilon = power")
print(f"       {gamma} x {epsilon} = {gamma * epsilon}")
