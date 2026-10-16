def test_case_1():
    assert equal(filter_a_keys(**{'d': {'ant': 10, 'bear': 20, 'ape': 30, 'cat': 40}}), {'ant': 10, 'ape': 30})
