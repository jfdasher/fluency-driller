def test_case_0():
    assert equal(append_to_copy(**{'data': [1, 2, 3]}), [[1, 2, 3], [1, 2, 3, 99]])
