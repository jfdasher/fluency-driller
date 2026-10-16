def test_case_3():
    assert equal(group_words_by_length(**{'words': ['a', 'b', 'c']}), {'1': ['a', 'b', 'c']})
