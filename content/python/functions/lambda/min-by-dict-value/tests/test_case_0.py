def test_case_0():
    assert equal(lowest_scorer(**{'scores': {'Alice': 88, 'Bob': 72, 'Carol': 95}}), 'Bob')
