def test_value_below_range():
    assert in_inclusive_range(0, 1, 10) == False
