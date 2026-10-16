def test_case_2():
    assert equal(top_n_common_numbers(**{'numbers': [7, 8, 7, 9, 8, 7, 9, 9, 9], 'n': 3}), [9, 7, 8])
