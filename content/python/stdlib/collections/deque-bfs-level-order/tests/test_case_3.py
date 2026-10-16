def test_case_3():
    assert equal(bfs_level_order(**{'edges': [['r', 's'], ['r', 't'], ['s', 'u'], ['t', 'v'], ['t', 'w']], 'root': 'r'}), ['r', 's', 't', 'u', 'v', 'w'])
