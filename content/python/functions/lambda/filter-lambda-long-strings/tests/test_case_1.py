def test_case_1():
    assert equal(keep_long(**{'words': ['a', 'bb', 'ccc', 'dddd'], 'min_len': 2}), ['ccc', 'dddd'])
