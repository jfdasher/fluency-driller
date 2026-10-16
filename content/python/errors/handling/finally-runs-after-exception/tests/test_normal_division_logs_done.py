def test_normal_division_logs_done():
    log = []
    result = safe_divide(10, 2, log)
    assert result == 5.0
    assert log == ['done']
