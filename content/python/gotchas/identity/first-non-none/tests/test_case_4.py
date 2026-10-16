def test_case_4():
    assert equal(first_non_none(**{'values': ['hello', None, 1]}), 'hello')
