def test_case_1():
    assert equal(filter_none_values(**{'values': [0, False, '', None]}), [None])
