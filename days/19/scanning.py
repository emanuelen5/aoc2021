from dataclasses import dataclass
import math
import numpy as np
from functools import cache
from typing import Union


@cache
def create_rot_mat(alpha: float, beta: float, gamma: float):
    rot_x = np.round(np.array([
        [1, 0, 0],
        [0, math.cos(alpha), -math.sin(alpha)],
        [0, math.sin(alpha), math.cos(alpha)]
    ]))
    rot_y = np.round(np.array([
        [math.cos(beta), 0, math.sin(beta)],
        [0, 1, 0],
        [-math.sin(beta), 0, math.cos(beta)]
    ]))
    rot_z = np.round(np.array([
        [math.cos(gamma), -math.sin(gamma), 0],
        [math.sin(gamma), math.cos(gamma), 0],
        [0, 0, 1]
    ]))
    rot_mat = rot_x @ rot_y @ rot_z  # @ is matrix multiplication
    return rot_mat


@dataclass
class Scanning:
    # scans: [n, 3] matrix with [x, y, z] coordinates for each scan
    scans: np.ndarray
    id: int = None

    def rotate(self, alpha: float, beta: float, gamma: float):
        """ Rotate in degrees around either axis """
        rot_mat = create_rot_mat(alpha * math.pi/180, beta * math.pi/180, gamma * math.pi/180)
        scans = np.matmul(self.scans, rot_mat)
        return self.__class__(scans, self.id)

    def create_rotation_permutations(self) -> list["Scanning"]:
        return [
            # 0
            self.rotate(0,     0, 0),
            self.rotate(90,    0, 0),
            self.rotate(180,   0, 0),
            self.rotate(270,   0, 0),
            # 4
            self.rotate(0,    90, 0),
            self.rotate(90,   90, 0),
            self.rotate(180,  90, 0),
            self.rotate(270,  90, 0),
            # 8
            self.rotate(0,   -90, 0),
            self.rotate(90,  -90, 0),
            self.rotate(180, -90, 0),
            self.rotate(270, -90, 0),
            # 12
            self.rotate(0,   180, 0),
            self.rotate(90,  180, 0),
            self.rotate(180, 180, 0),
            self.rotate(270, 180, 0),
            # 16
            self.rotate(0,   0,  90),
            self.rotate(90,  0,  90),
            self.rotate(180, 0,  90),
            self.rotate(270, 0,  90),
            # 20
            self.rotate(0,   0, -90),
            self.rotate(90,  0, -90),
            self.rotate(180, 0, -90),
            self.rotate(270, 0, -90),
        ]

    def copy(self) -> "Scanning":
        return Scanning(self.scans.copy(), self.id)

    def __add__(self, other):
        assert isinstance(other, np.ndarray)
        return Scanning(self.scans + other, self.id)

    def __sub__(self, other):
        assert isinstance(other, np.ndarray)
        return Scanning(self.scans - other, self.id)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return np.array_equiv(self.scans, other.scans) and self.id == other.id

    def __repr__(self):
        return f"<Scanning n_scans={len(self.scans)} id={self.id}>"

    def cross_correlate(self, other: "Scanning") -> tuple[int, tuple[int, int, int]]:
        max_equal = 0
        offset = (0, 0, 0)
        for row1 in self.scans:
            shifted1 = set((r[0], r[1], r[2]) for r in (self.scans - row1))
            for row2 in other.scans:
                shifted2 = set((r[0], r[1], r[2]) for r in (other.scans - row2))
                intersection = shifted1.intersection(shifted2)
                if len(intersection) > max_equal:
                    max_equal = len(intersection)
                    offset = row1 - row2

        return max_equal, tuple(offset)

    @classmethod
    def read_file(cls, filename: str) -> list["Scanning"]:
        import re
        with open(filename) as f:
            lines = f.read().splitlines()
        lines = [line for line in lines if len(line)]

        scan_pattern = re.compile(r"^--- scanner (\d+) ---$")
        scanning_values = id_ = None
        scannings = []
        for line in lines:
            if m := scan_pattern.match(line):
                if scanning_values is not None:
                    scanning_values = np.array(scanning_values)
                    scanning = Scanning(scanning_values, id_)
                    scannings.append(scanning)
                id_ = int(m.group(1))
                scanning_values = []
                continue
            scanning_values.append([int(v) for v in line.split(",")])
        return scannings
