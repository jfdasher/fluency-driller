def test_case_1():
    assert equal(highest_score(**{'records': [{'name': 'X', 'score': 10}]}), {'name': 'X', 'score': 10})
