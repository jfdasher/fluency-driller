def test_case_0():
    assert equal(filter_none_values(**{'values': [1, None, 'hello', None, 0]}), [None, None])
