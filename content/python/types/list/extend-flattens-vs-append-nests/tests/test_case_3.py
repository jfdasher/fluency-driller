def test_case_3():
    assert equal(add_flat(**{'base': ['a', 'b'], 'extra': ['c', 'd']}), ['a', 'b', 'c', 'd'])
