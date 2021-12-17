from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("--input_file", default=Path(__file__).parent / "data.txt")
args = parser.parse_args()

with open(args.input_file) as f:
    lines = f.readlines()

number_sum = 0
for line in lines:
    line = line[line.index("|") + 1:].strip()
    values = line.split(" ")
    digits = [s for s in values if len(s) in (2, 3, 4, 7)]
    number_sum += len(digits)

print(f"Part 1: {number_sum}")

number_signals = {0: "abcefg", 1: "cf", 2: "acdeg", 3: "acdfg", 4: "bcdf", 5: "abdfg", 6: "abdefg", 7: "acf",
                  8: "abcdefg", 9: "abcdfg"}
signals_number = {v: k for k, v in number_signals.items()}


def decode(numbers):
    occurances = dict(a=0, b=0, c=0, d=0, e=0, f=0, g=0)
    for number in numbers:
        for signal in number:
            occurances[signal] += 1

    def look_up_unique_value_from_map(map_: dict, value: int):
        for key, v in map_.items():
            if v == value:
                return key

    b = look_up_unique_value_from_map(occurances, 6)
    e = look_up_unique_value_from_map(occurances, 4)
    f = look_up_unique_value_from_map(occurances, 9)

    def lookup_unique_length_signals_from_number(letters, number: int):
        length = len(number_signals[number])
        for letter in letters:
            if len(letter) == length:
                return set(letter)

    signal_1 = lookup_unique_length_signals_from_number(numbers, 1)
    signal_7 = lookup_unique_length_signals_from_number(numbers, 7)
    signal_4 = lookup_unique_length_signals_from_number(numbers, 4)
    c = "".join(signal_1 - set(f))
    a = "".join(set(signal_7) - set(signal_1))
    d_and_g = {k for k, v in occurances.items() if v == 7}
    d = "".join(set(signal_4).intersection(d_and_g))
    g = "".join(d_and_g - set(d))

    return {a: "a", b: "b", c: "c", d: "d", e: "e", f: "f", g: "g"}


sum_ = 0
for line in lines:
    numbers, values = line.split("|")
    numbers = numbers.strip().split(" ")
    values = values.strip().split(" ")
    mapping = decode(numbers)
    translation_mapping = {ord(k): ord(v) for k, v in mapping.items()}
    translated_values = [v.translate(translation_mapping) for v in values]
    translated_sorted_values = ["".join(sorted(tv)) for tv in translated_values]
    print(f"From: {values}")
    print(f"Translated: {translated_sorted_values}")
    reverse_mapping = [signals_number[tsn] for tsn in translated_sorted_values]
    value = int("".join(str(s) for s in reverse_mapping))
    print(value)
    sum_ += value

print(f"Part 2: {sum_}")
