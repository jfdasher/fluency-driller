def test_case_3():
    assert equal(sort_keys_by_value_ascending(**{'d': {'dog': 2, 'cat': 2, 'ant': 2}}), ['ant', 'cat', 'dog'])
