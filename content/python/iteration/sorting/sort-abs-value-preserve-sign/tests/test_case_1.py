def test_case_1():
    assert equal(sort_abs_value_preserve_sign(**{'numbers': [-5, 5, -1, 1, 0]}), [0, -1, 1, -5, 5])
