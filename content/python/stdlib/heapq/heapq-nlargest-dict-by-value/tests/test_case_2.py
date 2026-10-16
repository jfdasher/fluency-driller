def test_case_2():
    assert equal(top_k_scores(**{'records': [{'name': 'A', 'score': 5}, {'name': 'B', 'score': 5}, {'name': 'C', 'score': 3}], 'k': 2}), [{'name': 'A', 'score': 5}, {'name': 'B', 'score': 5}])
