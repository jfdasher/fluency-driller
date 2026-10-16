def test_case_0():
    assert equal(keys_with_value(**{'d': {'a': 1, 'b': 2, 'c': 1, 'd': 3}, 'target': 1}), ['a', 'c'])
