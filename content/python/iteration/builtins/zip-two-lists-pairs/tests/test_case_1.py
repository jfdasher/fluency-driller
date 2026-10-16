def test_case_1():
    assert equal(pair_names_scores(**{'names': ['X', 'Y'], 'scores': [1, 2]}), [['X', 1], ['Y', 2]])
