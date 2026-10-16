def test_case_1():
    assert equal(first_mismatch_index(**{'a': [1, 2, 3], 'b': [1, 9, 3]}), 1)
