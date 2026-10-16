def test_case_2():
    assert equal(top_n_common_words(**{'words': ['x', 'y', 'z', 'x', 'y', 'x'], 'n': 3}), [['x', 3], ['y', 2], ['z', 1]])
