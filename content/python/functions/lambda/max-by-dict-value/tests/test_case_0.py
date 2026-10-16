def test_case_0():
    assert equal(highest_score(**{'records': [{'name': 'Alice', 'score': 88}, {'name': 'Bob', 'score': 95}, {'name': 'Carol', 'score': 72}]}), {'name': 'Bob', 'score': 95})
