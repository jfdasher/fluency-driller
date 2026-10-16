def test_missing_key_returns_default():
    assert get_value({}, 'x', 7) == 7
