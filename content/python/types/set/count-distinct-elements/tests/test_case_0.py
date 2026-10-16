def test_case_0():
    assert equal(count_distinct(**{'words': ['apple', 'banana', 'apple', 'cherry']}), 3)
