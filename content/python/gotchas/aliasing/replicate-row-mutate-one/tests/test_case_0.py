def test_case_0():
    assert equal(replicate_row_mutate_one(**{'row': [0, 0, 0], 'm': 3, 'col': 1, 'val': 9}), [[0, 9, 0], [0, 0, 0], [0, 0, 0]])
