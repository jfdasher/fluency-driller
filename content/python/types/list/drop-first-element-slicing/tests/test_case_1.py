def test_case_1():
    assert equal(drop_first(**{'lst': ['a', 'b', 'c']}), ['b', 'c'])
