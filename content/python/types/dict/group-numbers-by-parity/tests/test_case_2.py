def test_case_2():
    assert equal(group_numbers_by_parity(**{'numbers': [2, 4, 6]}), {'even': [2, 4, 6]})
