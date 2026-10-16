def test_case_0():
    assert equal(top_n_common_numbers(**{'numbers': [1, 2, 2, 3, 3, 3, 4], 'n': 2}), [3, 2])
