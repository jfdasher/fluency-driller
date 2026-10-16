def test_empty_string_fallback():
    assert get_username('') == 'Anonymous'
