def test_case_1():
    assert equal(word_frequency(**{'words': ['a', 'b', 'a', 'a', 'b']}), {'a': 3, 'b': 2})
