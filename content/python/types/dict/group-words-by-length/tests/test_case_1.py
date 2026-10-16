def test_case_1():
    assert equal(group_words_by_length(**{'words': ['hi', 'hello', 'hey', 'howdy', 'yo']}), {'2': ['hi', 'yo'], '5': ['hello', 'howdy'], '3': ['hey']})
