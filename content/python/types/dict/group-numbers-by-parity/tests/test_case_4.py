def test_case_4():
    assert equal(group_numbers_by_parity(**{'numbers': [0, -1, -2, 3]}), {'even': [0, -2], 'odd': [-1, 3]})
