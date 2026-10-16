def test_case_3():
    assert equal(countdown(**{'start': 20, 'stop': 5, 'step': 5}), [20, 15, 10, 5])
