def test_case_3():
    assert equal(drop_key(**{'d': {'a': 'hello'}, 'key': 'a', 'default': ''}), 'hello')
