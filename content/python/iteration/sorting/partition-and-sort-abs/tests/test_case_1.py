def test_case_1():
    assert equal(partition_and_sort_abs(**{'numbers': [-5, 5, -1, 1]}), {'positives': [1, 5], 'negatives': [-1, -5]})
