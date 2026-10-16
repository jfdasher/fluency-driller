def test_case_1():
    assert equal(count_distinct(**{'words': ['hello', 'hello', 'hello']}), 1)
