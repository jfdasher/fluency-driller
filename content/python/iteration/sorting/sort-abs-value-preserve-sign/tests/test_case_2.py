def test_case_2():
    assert equal(sort_abs_value_preserve_sign(**{'numbers': [4, -4, 2, -2]}), [-2, 2, -4, 4])
