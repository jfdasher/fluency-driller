def test_case_3():
    assert equal(set_ops(**{'a': [5, 1, 3, 2], 'b': [2, 3]}), {'intersection': [2, 3], 'union': [1, 2, 3, 5], 'difference': [1, 5]})
