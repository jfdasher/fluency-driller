def test_done_appended_exactly_once():
    log = []
    safe_divide(4, 2, log)
    assert len(log) == 1 and log[0] == 'done'
