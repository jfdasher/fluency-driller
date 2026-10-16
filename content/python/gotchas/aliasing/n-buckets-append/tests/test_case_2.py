def test_case_2():
    assert equal(fill_buckets(**{'n': 2, 'pairs': [[0, 1], [0, 2], [1, 3]]}), [[1, 2], [3]])
