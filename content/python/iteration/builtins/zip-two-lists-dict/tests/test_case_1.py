def test_case_1():
    assert equal(lists_to_dict(**{'keys': ['x', 'y'], 'values': [10, 20]}), {'x': 10, 'y': 20})
