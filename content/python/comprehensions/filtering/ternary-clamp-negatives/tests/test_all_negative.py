def test_all_negative():
    assert clamp_negatives([-5, -2, -9]) == [0, 0, 0]
