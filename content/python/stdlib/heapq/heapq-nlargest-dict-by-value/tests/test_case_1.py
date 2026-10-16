def test_case_1():
    assert equal(top_k_scores(**{'records': [{'name': 'X', 'score': 10}, {'name': 'Y', 'score': 50}, {'name': 'Z', 'score': 30}], 'k': 1}), [{'name': 'Y', 'score': 50}])
