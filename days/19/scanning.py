from dataclasses import dataclass
import math
import numpy as np
from functools import cache


@cache
def create_rot_mat(alpha: float, beta: float, gamma: float):
    rot_x = np.ndarray([
        [1, 0, 0],
        [0, math.cos(alpha), -math.sin(alpha)],
        [0, math.sin(alpha), math.cos(alpha)]
    ])
    rot_y = np.ndarray([
        [math.cos(beta), 0, math.sin(beta)],
        [0, 1, 0],
        [-math.sin(beta), 0, math.cos(beta)]
    ])
    rot_z = np.ndarray([
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
        rot_mat = create_rot_mat(alpha, beta, gamma)
        scans = self.scans * rot_mat
        return self.__class__(scans)

    def create_rotation_permutations(self) -> list["Scanning"]:
        pass

    def __repr__(self):
        return f"<Scanning n_scans={len(self.scans)} id={self.id}>"
