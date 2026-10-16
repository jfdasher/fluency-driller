def test_case_0():
    assert equal(add_flat(**{'base': [1, 2, 3], 'extra': [4, 5]}), [1, 2, 3, 4, 5])
