def test_case_0():
    assert equal(record_snapshots(**{'ops': [1, 2, 3]}), [[1], [1, 2], [1, 2, 3]])
