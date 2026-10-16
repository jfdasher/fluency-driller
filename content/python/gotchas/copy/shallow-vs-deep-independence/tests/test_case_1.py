def test_case_1():
    assert equal(safe_clone(**{'grid': [[7, 8, 9], [10, 11, 12]]}), [[[99, 8, 9], [10, 11, 12]], True])
