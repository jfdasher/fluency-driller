def test_case_1():
    assert equal(replicate_row_mutate_one(**{'row': [1, 2, 3], 'm': 4, 'col': 0, 'val': 7}), [[7, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]])
