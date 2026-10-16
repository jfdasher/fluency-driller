def test_case_1():
    assert equal(name_score_dict(**{'names': ['x'], 'scores': [42]}), {'x': 42})
