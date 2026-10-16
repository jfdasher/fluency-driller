def test_case_0():
    assert equal(invert_dict(**{'d': {'a': 'one', 'b': 'two', 'c': 'three'}}), {'one': 'a', 'two': 'b', 'three': 'c'})
