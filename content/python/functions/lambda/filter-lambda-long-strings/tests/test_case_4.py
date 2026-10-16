def test_case_4():
    assert equal(keep_long(**{'words': ['one', 'two', 'three'], 'min_len': 10}), [])
