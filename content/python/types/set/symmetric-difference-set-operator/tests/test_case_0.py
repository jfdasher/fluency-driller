def test_case_0():
    assert equal(sym_diff(**{'a': [1, 2, 3, 4], 'b': [3, 4, 5, 6]}), [1, 2, 5, 6])
