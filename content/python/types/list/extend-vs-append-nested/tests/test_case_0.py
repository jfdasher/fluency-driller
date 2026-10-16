def test_case_0():
    assert equal(add_as_element(**{'base': [1, 2, 3], 'extra': [4, 5]}), [1, 2, 3, [4, 5]])
