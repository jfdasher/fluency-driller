def test_case_0():
    assert equal(count_items(**{'items': ['a', 'b', 'a', 'c', 'b', 'a']}), {'a': 3, 'b': 2, 'c': 1})
