def test_case_1():
    assert equal(invert_dict(**{'d': {'x': 'alpha', 'y': 'beta'}}), {'alpha': 'x', 'beta': 'y'})
