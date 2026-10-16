def test_case_2():
    assert equal(drop_key(**{'d': {}, 'key': 'k', 'default': 0}), 0)
