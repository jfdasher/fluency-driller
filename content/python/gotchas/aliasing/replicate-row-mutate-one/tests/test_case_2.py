def test_case_2():
    assert equal(replicate_row_mutate_one(**{'row': [5], 'm': 2, 'col': 0, 'val': 0}), [[0], [5]])
