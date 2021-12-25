from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.read().splitlines()


def deconstruct(s: str):
    version = int(s[:3], 2)
    type_id = int(s[3:6], 2)
    if type_id == 4:  # Literal value
        const = ""
        i = 6
        while i < len(s):
            const += s[i+1:i+5]
            i += 5
            if i == 0:
                break
        print(f"{const=}")
        const = int(const, 2)
        print(f"{const=}")
    else:
        length_id = s[6]
        if length_id == "0":
            subpacket_len = int(s[7:7 + 15], 2)
            print(f"{subpacket_len=}")
            deconstruct(s[7+15:])
        else:
            subpacket_count = int(s[7:7+11], 2)
            print(f"{subpacket_count=}")
            deconstruct(s[7+11:])


for line in lines:
    data = bytearray.fromhex(line)
    bits = "".join(f"{d:08b}" for d in data).rstrip("0")
    print(deconstruct(bits))

print(f"Part 1: {0}\n")
print(f"Part 2: {0}\n")
