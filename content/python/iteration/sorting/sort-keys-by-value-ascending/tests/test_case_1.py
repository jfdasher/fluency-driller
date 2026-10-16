def test_case_1():
    assert equal(sort_keys_by_value_ascending(**{'d': {'b': 5, 'a': 5, 'c': 3}}), ['c', 'a', 'b'])
