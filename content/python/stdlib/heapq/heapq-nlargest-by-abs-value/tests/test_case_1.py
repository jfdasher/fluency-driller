def test_case_1():
    assert equal(top_k_by_abs(**{'nums': [10, -20, 15, -1], 'k': 2}), [-20, 15])
