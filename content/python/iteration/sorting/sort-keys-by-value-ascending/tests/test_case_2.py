def test_case_2():
    assert equal(sort_keys_by_value_ascending(**{'d': {'x': 10, 'y': 1, 'z': 5}}), ['y', 'z', 'x'])
