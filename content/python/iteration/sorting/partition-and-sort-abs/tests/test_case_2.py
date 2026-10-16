def test_case_2():
    assert equal(partition_and_sort_abs(**{'numbers': [4, 2, 6]}), {'positives': [2, 4, 6], 'negatives': []})
