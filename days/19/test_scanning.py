import numpy as np
from scanning import Scanning


def test_rotation():
    scanning = Scanning(np.array([[1, 1, 1]]), 1)
    assert scanning.rotate(360, 0, 0) == scanning
    assert scanning.rotate(0, 360, 0) == scanning
    assert scanning.rotate(0, 0, 360) == scanning
