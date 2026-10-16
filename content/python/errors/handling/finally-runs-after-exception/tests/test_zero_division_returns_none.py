def test_zero_division_returns_none():
    log = []
    result = safe_divide(7, 0, log)
    assert result is None
