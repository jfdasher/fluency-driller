def test_case_3():
    assert equal(replicate_row_mutate_one(**{'row': [0, 0], 'm': 1, 'col': 1, 'val': 42}), [[0, 42]])
