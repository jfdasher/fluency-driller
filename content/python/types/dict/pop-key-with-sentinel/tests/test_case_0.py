def test_case_0():
    assert equal(drop_key(**{'d': {'x': 10, 'y': 20}, 'key': 'x', 'default': -1}), 10)
