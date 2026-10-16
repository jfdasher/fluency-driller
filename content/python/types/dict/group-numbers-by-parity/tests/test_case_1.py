def test_case_1():
    assert equal(group_numbers_by_parity(**{'numbers': [10, 7, 4, 3]}), {'even': [10, 4], 'odd': [7, 3]})
