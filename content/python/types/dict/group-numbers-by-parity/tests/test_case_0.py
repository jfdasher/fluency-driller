def test_case_0():
    assert equal(group_numbers_by_parity(**{'numbers': [1, 2, 3, 4, 5, 6]}), {'odd': [1, 3, 5], 'even': [2, 4, 6]})
