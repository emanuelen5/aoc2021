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
        return length, version, const
    else:
        length_id = s[6]
        subpacket_values = []
        if length_id == "0":
            length = 7 + 15
            subpacket_len = int(s[7:length], 2)
            parsed_len = 0
            while parsed_len < subpacket_len:
                length_, version_, value = deconstruct(s[length + parsed_len:])
                subpacket_values.append(value)
                parsed_len += length_
                version = version + version_
            length = length + parsed_len
        else:
            length = 7 + 11
            subpacket_count = int(s[7:length], 2)
            for i in range(subpacket_count):
                length_, version_, value = deconstruct(s[length:])
                subpacket_values.append(value)
                version += version_
                length += length_
        if type_id == 0:
            return length, version, sum(subpacket_values)
        elif type_id == 1:
            product = subpacket_values[0]
            for p in subpacket_values[1:]:
                product *= p
            return length, version, product
        elif type_id == 2:
            return length, version, min(subpacket_values)
        elif type_id == 3:
            return length, version, max(subpacket_values)
        elif type_id == 5:
            if len(subpacket_values) != 2:
                raise RuntimeError(f"Wrong number of subpackets. Got {len(subpacket_values)}")
            return length, version, 1 if subpacket_values[0] > subpacket_values[1] else 0
        elif type_id == 6:
            if len(subpacket_values) != 2:
                raise RuntimeError(f"Wrong number of subpackets. Got {len(subpacket_values)}")
            return length, version, 1 if subpacket_values[0] < subpacket_values[1] else 0
        elif type_id == 7:
            if len(subpacket_values) != 2:
                raise RuntimeError(f"Wrong number of subpackets. Got {len(subpacket_values)}")
            return length, version, 1 if subpacket_values[0] == subpacket_values[1] else 0
        raise RuntimeError(f"Logic error. Got packet type {type_id}")


for line in lines:
    data = bytearray.fromhex(line)
    bits = "".join(f"{d:08b}" for d in data)
    length, version, value = deconstruct(bits)
    print(f"\nPacket: {line}")
    print(f"\tbits: {bits}")
    print(f"Part 1. Version sum: {version}")
    print(f"Part 2: Value: {value}\n")
