def test_case_0():
    assert equal(partition_and_sort_abs(**{'numbers': [3, -1, -3, 2, -2, 0]}), {'positives': [0, 2, 3], 'negatives': [-1, -2, -3]})
