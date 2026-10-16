def test_case_0():
    assert equal(number_items(**{'items': ['a', 'b', 'c']}), [[1, 'a'], [2, 'b'], [3, 'c']])
