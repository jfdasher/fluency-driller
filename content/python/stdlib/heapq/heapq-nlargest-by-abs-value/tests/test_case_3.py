def test_case_3():
    assert equal(top_k_by_abs(**{'nums': [1, -1, 2, -2], 'k': 4}), [2, -2, 1, -1])
