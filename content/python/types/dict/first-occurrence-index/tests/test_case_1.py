def test_case_1():
    assert equal(first_occurrence_index(**{'items': ['x', 'x', 'x']}), {'x': 0})
