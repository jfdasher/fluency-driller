def test_case_1():
    assert equal(first_non_none(**{'values': [None, 0, None]}), 0)
