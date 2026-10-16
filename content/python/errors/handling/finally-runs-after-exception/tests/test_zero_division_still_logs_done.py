def test_zero_division_still_logs_done():
    log = []
    safe_divide(7, 0, log)
    assert log == ['done']
