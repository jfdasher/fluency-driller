def test_mixed():
    assert clamp_negatives([-3, 1, -1, 4, 0]) == [0, 1, 0, 4, 0]
