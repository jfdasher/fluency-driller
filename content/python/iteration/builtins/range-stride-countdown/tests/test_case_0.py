def test_case_0():
    assert equal(countdown(**{'start': 10, 'stop': 1, 'step': 3}), [10, 7, 4, 1])
