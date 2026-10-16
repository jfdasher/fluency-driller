def test_case_1():
    assert equal(record_snapshots(**{'ops': [5]}), [[5]])
