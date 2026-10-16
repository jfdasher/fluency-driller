def test_case_3():
    assert equal(top_n_common_words(**{'words': ['dog', 'cat', 'dog', 'dog', 'cat'], 'n': 2}), [['dog', 3], ['cat', 2]])
