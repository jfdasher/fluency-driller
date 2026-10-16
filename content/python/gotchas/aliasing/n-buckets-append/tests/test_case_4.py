def test_case_4():
    assert equal(fill_buckets(**{'n': 3, 'pairs': [[2, 99], [1, 42], [2, 7]]}), [[], [42], [99, 7]])
