from dataclasses import dataclass
import math
import numpy as np
from functools import cache


@cache
def create_rot_mat(alpha: float, beta: float, gamma: float):
    rot_x = np.array([
        [1, 0, 0],
        [0, math.cos(alpha), -math.sin(alpha)],
        [0, math.sin(alpha), math.cos(alpha)]
    ])
    rot_y = np.array([
        [math.cos(beta), 0, math.sin(beta)],
        [0, 1, 0],
        [-math.sin(beta), 0, math.cos(beta)]
    ])
    rot_z = np.array([
        [math.cos(gamma), -math.sin(gamma), 0],
        [math.sin(gamma), math.cos(gamma), 0],
        [0, 0, 1]
    ])
    return rot_z * rot_y * rot_x


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
        pass

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return np.array_equiv(self.scans, other.scans) and self.id == other.id

    def __repr__(self):
        return f"<Scanning n_scans={len(self.scans)} id={self.id}>"

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
