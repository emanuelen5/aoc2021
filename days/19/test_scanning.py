import numpy as np
import pytest
from scanning import Scanning

np.random.seed(1)


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


@pytest.fixture
def scanning_origin():
    return Scanning(np.array([
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1],
    ]))


def test_cross_correlate_translation(scanning_origin):
    offset = [1, 1, 1]
    scanning2 = scanning_origin - np.array(offset)
    count, corr_offset = scanning_origin.cross_correlate(scanning2)
    assert count == len(scanning_origin.scans)
    assert corr_offset == tuple(offset)


def test_cross_correlate_translation_random_permutation(scanning_origin):
    offset = [1, 1, 1]
    scans = scanning_origin.scans - np.array(offset)
    scans = np.random.permutation(scans)
    scanning2 = Scanning(scans, scanning_origin.id)
    count, corr_offset = scanning_origin.cross_correlate(scanning2)
    assert count == len(scanning_origin.scans)
    assert corr_offset == tuple(offset)


def test_cross_correlate_translation_random_permutation_extras(scanning_origin):
    offset = [1, 1, 1]
    scans = scanning_origin.scans
    scans = np.vstack((scans, [[0, -1, -1], [0, 5, 5], [1, 5, 5], [2, 5, 5]]))
    scans = scans - np.array(offset)
    scans = np.random.permutation(scans)
    scanning2 = Scanning(scans, scanning_origin.id)
    count, corr_offset = scanning_origin.cross_correlate(scanning2)
    assert count == len(scanning_origin.scans)
    assert corr_offset == tuple(offset)
