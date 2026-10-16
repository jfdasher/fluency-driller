def test_case_1():
    assert equal(keys_with_value(**{'d': {'x': 5, 'y': 5, 'z': 5}, 'target': 5}), ['x', 'y', 'z'])
