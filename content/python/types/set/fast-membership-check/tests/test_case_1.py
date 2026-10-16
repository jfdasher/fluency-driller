def test_case_1():
    assert equal(is_allowed(**{'allowed': ['alice', 'bob', 'carol'], 'username': 'dave'}), False)
