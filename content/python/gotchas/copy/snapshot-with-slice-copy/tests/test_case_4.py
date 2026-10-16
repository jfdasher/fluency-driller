def test_case_4():
    assert equal(record_snapshots(**{'ops': [3, 1, 4, 1, 5]}), [[3], [3, 1], [3, 1, 4], [3, 1, 4, 1], [3, 1, 4, 1, 5]])
