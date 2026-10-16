def test_case_1():
    assert equal(add_flat(**{'base': [1, 2, 3], 'extra': []}), [1, 2, 3])
