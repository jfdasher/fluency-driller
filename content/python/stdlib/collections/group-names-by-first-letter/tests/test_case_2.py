def test_case_2():
    assert equal(group_names_by_first_letter(**{'names': ['Maria']}), {'M': ['Maria']})
