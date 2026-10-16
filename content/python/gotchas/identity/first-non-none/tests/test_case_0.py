def test_case_0():
    assert equal(first_non_none(**{'values': [None, None, 42, None]}), 42)
