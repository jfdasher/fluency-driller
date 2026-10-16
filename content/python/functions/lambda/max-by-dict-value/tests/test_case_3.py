def test_case_3():
    assert equal(highest_score(**{'records': [{'name': 'P', 'score': 0}, {'name': 'Q', 'score': -5}, {'name': 'R', 'score': 3}]}), {'name': 'R', 'score': 3})
