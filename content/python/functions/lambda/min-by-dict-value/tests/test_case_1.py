def test_case_1():
    assert equal(lowest_scorer(**{'scores': {'Alice': 50, 'Bob': 50, 'Carol': 99}}), 'Alice')
