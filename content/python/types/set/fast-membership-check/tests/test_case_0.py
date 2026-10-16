def test_case_0():
    assert equal(is_allowed(**{'allowed': ['alice', 'bob', 'carol'], 'username': 'bob'}), True)
