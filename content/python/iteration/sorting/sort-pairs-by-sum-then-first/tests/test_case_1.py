def test_case_1():
    assert equal(sort_pairs_by_sum_then_first(**{'pairs': [[3, 3], [1, 5], [2, 4], [0, 6]]}), [[0, 6], [1, 5], [2, 4], [3, 3]])
