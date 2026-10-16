def test_case_0():
    assert equal(fill_buckets(**{'n': 3, 'pairs': [[0, 'a'], [1, 'b'], [0, 'c'], [2, 'd']]}), [['a', 'c'], ['b'], ['d']])
