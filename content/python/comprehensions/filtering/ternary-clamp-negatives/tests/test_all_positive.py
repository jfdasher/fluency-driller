def test_all_positive():
    assert clamp_negatives([1, 2, 3]) == [1, 2, 3]
