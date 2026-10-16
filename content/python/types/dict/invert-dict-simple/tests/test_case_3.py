def test_case_3():
    assert equal(invert_dict(**{'d': {'only': 'one'}}), {'one': 'only'})
