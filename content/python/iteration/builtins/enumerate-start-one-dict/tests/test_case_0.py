def test_case_0():
    assert equal(index_from_one(**{'items': ['apple', 'banana', 'cherry']}), {'1': 'apple', '2': 'banana', '3': 'cherry'})
