def test_case_0():
    assert equal(keep_long(**{'words': ['hi', 'hello', 'hey', 'greetings'], 'min_len': 3}), ['hello', 'greetings'])
