def test_zero_fallback():
    assert get_username(0) == 'Anonymous'
