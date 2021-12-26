from solution import calc_magnitude


def test_magnitude():
    assert 143 == calc_magnitude([[1,2],[[3,4],5]])
    assert 1384 == calc_magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
    assert 445 == calc_magnitude([[[[1,1],[2,2]],[3,3]],[4,4]])
