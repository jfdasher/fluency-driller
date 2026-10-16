def test_none_fallback():
    assert get_username(None) == 'Anonymous'
