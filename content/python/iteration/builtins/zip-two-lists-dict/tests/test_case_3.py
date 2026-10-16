def test_case_3():
    assert equal(lists_to_dict(**{'keys': ['only'], 'values': [42]}), {'only': 42})
