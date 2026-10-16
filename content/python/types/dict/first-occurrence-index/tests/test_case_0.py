def test_case_0():
    assert equal(first_occurrence_index(**{'items': ['a', 'b', 'a', 'c', 'b']}), {'a': 0, 'b': 1, 'c': 3})
