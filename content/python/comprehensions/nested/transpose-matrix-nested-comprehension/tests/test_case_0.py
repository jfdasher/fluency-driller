def test_case_0():
    assert equal(transpose(**{'matrix': [[1, 2, 3], [4, 5, 6]]}), [[1, 4], [2, 5], [3, 6]])
