def test_case_1():
    assert equal(bfs_level_order(**{'edges': [['1', '2'], ['1', '3'], ['3', '4']], 'root': '1'}), ['1', '2', '3', '4'])
