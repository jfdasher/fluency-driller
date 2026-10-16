def test_case_3():
    assert equal(first_non_none(**{'values': [None, None, None]}), None)
