def test_case_1():
    assert equal(set_ops(**{'a': [1, 2, 3], 'b': [4, 5, 6]}), {'intersection': [], 'union': [1, 2, 3, 4, 5, 6], 'difference': [1, 2, 3]})
