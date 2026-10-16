def test_case_4():
    assert equal(append_to_copy(**{'data': ['x', 'y', 'z']}), [['x', 'y', 'z'], ['x', 'y', 'z', 99]])
