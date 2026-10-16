def test_case_0():
    assert equal(top_n_common_words(**{'words': ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple'], 'n': 2}), [['apple', 3], ['banana', 2]])
