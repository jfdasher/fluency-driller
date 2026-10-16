def test_case_1():
    assert equal(countdown(**{'start': 5, 'stop': 1, 'step': 1}), [5, 4, 3, 2, 1])
