import numpy as np
from scanning import Scanning


def test_rotation():
    scanning = Scanning(np.array([[1, 1, 1]]), 1)
    assert scanning.rotate(360, 0, 0) == scanning, f"{scanning=}"
    assert scanning.rotate(0, 360, 0) == scanning, f"{scanning=}"
    assert scanning.rotate(0, 0, 360) == scanning, f"{scanning=}"


def test_unique_rotation_permutations():
    scanning = Scanning(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), 1)
    assert scanning.create_rotation_permutations() == scanning.create_rotation_permutations()
    scannings = scanning.create_rotation_permutations()
    for i, scan1 in enumerate(scannings):
        for j, scan2 in enumerate(scannings):
            if i == j:
                assert scan1 == scan2, f"{i=}, {j=}: {scan1.scans=}, {scan2.scans=}"
            else:
                assert scan1 != scan2, f"{i=}, {j=}: {scan1.scans=}, {scan2.scans=}"
