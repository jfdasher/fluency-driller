def test_datetime_value():
    import json, datetime
    dt = datetime.datetime(2024, 1, 15, 10, 30, 0)
    result = fn({'ts': dt})
    parsed = json.loads(result)
    assert parsed['ts'] == '2024-01-15T10:30:00'
