def test_case_2():
    assert equal(first_non_none(**{'values': [None, False, None]}), False)
