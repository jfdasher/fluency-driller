def test_nested_datetime():
    import json, datetime
    dt1 = datetime.datetime(2000, 6, 1, 0, 0, 0)
    dt2 = datetime.datetime(1999, 12, 31, 23, 59, 59)
    result = fn([dt1, dt2])
    parsed = json.loads(result)
    assert parsed == ['2000-06-01T00:00:00', '1999-12-31T23:59:59']
