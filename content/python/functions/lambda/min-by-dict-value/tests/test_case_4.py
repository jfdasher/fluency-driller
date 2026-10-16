def test_case_4():
    assert equal(lowest_scorer(**{'scores': {'x': 100, 'y': 200, 'z': 0}}), 'z')
