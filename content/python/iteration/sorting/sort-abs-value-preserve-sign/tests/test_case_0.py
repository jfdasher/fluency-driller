def test_case_0():
    assert equal(sort_abs_value_preserve_sign(**{'numbers': [3, -1, -3, 2, -2]}), [-1, -2, 2, -3, 3])
