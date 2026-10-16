def test_case_2():
    assert equal(set_ops(**{'a': [1, 2, 3], 'b': [1, 2, 3]}), {'intersection': [1, 2, 3], 'union': [1, 2, 3], 'difference': []})
