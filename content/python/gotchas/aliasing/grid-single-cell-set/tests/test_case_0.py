def test_case_0():
    assert equal(set_cell(**{'m': 3, 'n': 3, 'row': 1, 'col': 1, 'val': 9}), [[0, 0, 0], [0, 9, 0], [0, 0, 0]])
