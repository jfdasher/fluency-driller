def test_case_1():
    assert equal(value_to_index(**{'items': ['x', 'y', 'z']}), {'x': 0, 'y': 1, 'z': 2})
