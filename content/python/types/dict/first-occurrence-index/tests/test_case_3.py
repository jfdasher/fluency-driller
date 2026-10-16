def test_case_3():
    assert equal(first_occurrence_index(**{'items': ['hello', 'world', 'hello', 'python']}), {'hello': 0, 'world': 1, 'python': 3})
