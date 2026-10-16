def test_case_3():
    assert equal(filter_none_values(**{'values': [None, None, None]}), [None, None, None])
