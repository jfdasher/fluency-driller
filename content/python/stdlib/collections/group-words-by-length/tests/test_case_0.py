def test_case_0():
    assert equal(group_words_by_length(**{'words': ['cat', 'dog', 'elephant', 'ox', 'ant', 'be']}), {'3': ['cat', 'dog', 'ant'], '8': ['elephant'], '2': ['ox', 'be']})
