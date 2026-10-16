def test_case_3():
    assert equal(record_snapshots(**{'ops': [10, 20]}), [[10], [10, 20]])
