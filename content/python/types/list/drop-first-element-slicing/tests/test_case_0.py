def test_case_0():
    assert equal(drop_first(**{'lst': [1, 2, 3, 4]}), [2, 3, 4])
