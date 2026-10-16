def test_case_2():
    assert equal(keep_long(**{'words': ['cat', 'dog', 'elephant'], 'min_len': 5}), ['elephant'])
