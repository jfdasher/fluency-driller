def test_case_1():
    assert equal(drop_last(**{'lst': ['a', 'b', 'c']}), ['a', 'b'])
