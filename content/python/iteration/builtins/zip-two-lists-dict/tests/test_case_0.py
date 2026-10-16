def test_case_0():
    assert equal(lists_to_dict(**{'keys': ['a', 'b', 'c'], 'values': [1, 2, 3]}), {'a': 1, 'b': 2, 'c': 3})
