def test_sep_overridden():
    result = call_with_dot()
    assert '.' in result
    assert '-' not in result
