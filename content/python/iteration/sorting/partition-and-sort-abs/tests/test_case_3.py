def test_case_3():
    assert equal(partition_and_sort_abs(**{'numbers': [-4, -2, -6]}), {'positives': [], 'negatives': [-2, -4, -6]})
