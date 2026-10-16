def test_case_1():
    assert equal(group_words_by_length(**{'words': ['a', 'bb', 'ccc', 'dd', 'e']}), {'1': ['a', 'e'], '2': ['bb', 'dd'], '3': ['ccc']})
