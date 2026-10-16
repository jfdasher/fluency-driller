def test_case_3():
    assert equal(add_as_element(**{'base': ['a', 'b'], 'extra': ['c']}), ['a', 'b', ['c']])
