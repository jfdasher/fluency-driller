def test_case_2():
    assert equal(sym_diff(**{'a': [1, 2, 3], 'b': [4, 5, 6]}), [1, 2, 3, 4, 5, 6])
