def test_case_0():
    assert equal(top_k_scores(**{'records': [{'name': 'Alice', 'score': 88}, {'name': 'Bob', 'score': 95}, {'name': 'Carol', 'score': 72}], 'k': 2}), [{'name': 'Bob', 'score': 95}, {'name': 'Alice', 'score': 88}])
