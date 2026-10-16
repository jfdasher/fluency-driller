def test_case_1():
    assert equal(top_n_common_words(**{'words': ['a', 'b', 'a', 'c', 'b', 'a'], 'n': 1}), [['a', 3]])
