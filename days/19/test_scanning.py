import numpy as np
from pathlib import Path
import pytest
import random
from scanning import Scanning

_seed = 1
np.random.seed(_seed)
random.seed(_seed)


def test_read_from_file():
    scannings = Scanning.read_file(str((Path(__file__).parent.joinpath("test_data.txt").absolute())))
    assert len(scannings) == 5


def test_rotation():
    scanning = Scanning(np.array([[1, 1, 1]]), 1)
    assert scanning.rotate(360, 0, 0) == scanning, f"{scanning=}"
    assert scanning.rotate(0, 360, 0) == scanning, f"{scanning=}"
    assert scanning.rotate(0, 0, 360) == scanning, f"{scanning=}"


def test_unique_rotation_permutations():
    scanning = Scanning(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), 1)
    assert scanning.create_rotation_permutations() == scanning.create_rotation_permutations()
    scannings = scanning.create_rotation_permutations()
    for i, (angles1, scan1) in enumerate(scannings):
        for j, (angles2, scan2) in enumerate(scannings):
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
        [1, 1, 10],
    ]), id=5000)


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
    scans = np.vstack((scanning_origin.scans, [[0, -1, -1], [0, 5, 5], [1, 5, 5], [2, 5, 5]]))
    scans = scans - np.array(offset)
    scans = np.random.permutation(scans)
    scanning2 = Scanning(scans, scanning_origin.id)
    count, corr_offset = scanning_origin.cross_correlate(scanning2)
    assert count == len(scanning_origin.scans)
    assert corr_offset == tuple(offset)


def test_find_cross_correlation(scanning_origin):
    offset = np.array([1, 1, 1])
    angle, scanning2 = random.choice(scanning_origin.create_rotation_permutations())
    scanning2 = scanning2 - offset
    count, corr_angle, corr_offset = scanning_origin.find_cross_correlation(scanning2, threshold=None)
    assert count == len(scanning_origin.scans)
    assert corr_angle == angle
    assert corr_offset == tuple(offset)
