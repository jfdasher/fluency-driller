def test_case_0():
    assert equal(value_to_index(**{'items': ['apple', 'banana', 'cherry']}), {'apple': 0, 'banana': 1, 'cherry': 2})
