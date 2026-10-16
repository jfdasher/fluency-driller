def test_case_2():
    assert equal(sort_pairs_by_sum_then_first(**{'pairs': [[5, 0], [3, 2], [4, 1]]}), [[3, 2], [4, 1], [5, 0]])
