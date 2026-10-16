def test_case_0():
    assert equal(safe_clone(**{'grid': [[1, 2], [3, 4]]}), [[[99, 2], [3, 4]], True])
