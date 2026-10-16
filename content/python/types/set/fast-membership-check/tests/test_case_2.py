def test_case_2():
    assert equal(is_allowed(**{'allowed': [], 'username': 'alice'}), False)
