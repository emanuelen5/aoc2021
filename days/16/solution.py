from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("--input-file", "-i", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = [l for l in f.read().splitlines() if not l.startswith("#")]


def deconstruct(s: str):
    version = int(s[:3], 2)
    type_id = int(s[3:6], 2)
    if type_id == 4:  # Literal value
        const = ""
        length = 6
        last = False
        while not last:
            last = s[length] == '0'
            const += s[length+1:length+5]
            length += 5
        const = int(const, 2)
        print(f"Constant packet: {const=}")
        return length, version
    else:
        length_id = s[6]
        if length_id == "0":
            length = 7 + 15
            subpacket_len = int(s[7:length], 2)
            parsed_len = 0
            while parsed_len < subpacket_len:
                print(f"Subpacket {parsed_len}/{subpacket_len} length {{")
                length_, version_ = deconstruct(s[length + parsed_len:])
                print("}")
                parsed_len += length_
                version = version + version_
            return length + parsed_len, version
        else:
            length = 7 + 11
            subpacket_count = int(s[7:length], 2)
            for i in range(subpacket_count):
                print(f"Subpacket {i+1}/{subpacket_count} count {{")
                length_, version_ = deconstruct(s[length:])
                print("}")
                version += version_
                length += length_
            return length, version


for line in lines:
    data = bytearray.fromhex(line)
    bits = "".join(f"{d:08b}" for d in data).rstrip("0")
    length, version = deconstruct(bits)
    print(f"Part 1. Version sum: {version}")

print(f"Part 2: {0}\n")
