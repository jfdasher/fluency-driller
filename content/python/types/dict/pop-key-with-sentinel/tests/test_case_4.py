def test_case_4():
    assert equal(drop_key(**{'d': {'a': 'hello'}, 'key': 'b', 'default': 'missing'}), 'missing')
