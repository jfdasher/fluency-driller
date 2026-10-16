def test_case_3():
    assert equal(group_words_by_length(**{'words': ['hello', 'world', 'hi']}), {'5': ['hello', 'world'], '2': ['hi']})
