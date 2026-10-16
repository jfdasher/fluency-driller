def test_case_1():
    assert equal(drop_key(**{'d': {'x': 10, 'y': 20}, 'key': 'z', 'default': -1}), -1)
