def test_case_0():
    assert equal(set_ops(**{'a': [1, 2, 3, 4], 'b': [3, 4, 5, 6]}), {'intersection': [3, 4], 'union': [1, 2, 3, 4, 5, 6], 'difference': [1, 2]})
