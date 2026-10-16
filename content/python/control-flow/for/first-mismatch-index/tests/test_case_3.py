def test_case_3():
    assert equal(first_mismatch_index(**{'a': [0, 0, 0, 1], 'b': [0, 0, 0, 0]}), 3)
