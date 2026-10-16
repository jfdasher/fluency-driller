def test_case_3():
    assert equal(append_to_copy(**{'data': [10, 20]}), [[10, 20], [10, 20, 99]])
