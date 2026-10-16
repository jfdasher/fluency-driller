def test_case_0():
    assert equal(top_k_by_abs(**{'nums': [1, -5, 3, -2, 4], 'k': 3}), [-5, 4, 3])
