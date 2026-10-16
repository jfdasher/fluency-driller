def test_case_0():
    assert equal(bfs_level_order(**{'edges': [['a', 'b'], ['a', 'c'], ['b', 'd'], ['b', 'e']], 'root': 'a'}), ['a', 'b', 'c', 'd', 'e'])
