def test_case_0():
    assert equal(sort_pairs_by_sum_then_first(**{'pairs': [[1, 3], [2, 2], [0, 4], [1, 1]]}), [[1, 1], [0, 4], [1, 3], [2, 2]])
