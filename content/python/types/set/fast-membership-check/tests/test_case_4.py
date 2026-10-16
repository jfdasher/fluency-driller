def test_case_4():
    assert equal(is_allowed(**{'allowed': ['x', 'y', 'z'], 'username': 'a'}), False)
