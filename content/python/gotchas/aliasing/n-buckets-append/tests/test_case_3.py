def test_case_3():
    assert equal(fill_buckets(**{'n': 1, 'pairs': [[0, 'x'], [0, 'y']]}), [['x', 'y']])
