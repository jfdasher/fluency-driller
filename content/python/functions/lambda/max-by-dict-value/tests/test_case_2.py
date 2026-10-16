def test_case_2():
    assert equal(highest_score(**{'records': [{'name': 'A', 'score': 50}, {'name': 'B', 'score': 50}, {'name': 'C', 'score': 49}]}), {'name': 'A', 'score': 50})
