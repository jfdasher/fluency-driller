def test_case_0():
    assert equal(sort_keys_by_value_ascending(**{'d': {'banana': 3, 'apple': 1, 'cherry': 2}}), ['apple', 'cherry', 'banana'])
