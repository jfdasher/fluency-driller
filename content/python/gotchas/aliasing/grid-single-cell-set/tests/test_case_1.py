def test_case_1():
    assert equal(set_cell(**{'m': 2, 'n': 4, 'row': 0, 'col': 2, 'val': 5}), [[0, 0, 5, 0], [0, 0, 0, 0]])
