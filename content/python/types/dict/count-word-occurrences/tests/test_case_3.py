def test_case_3():
    assert equal(count_words(**{'words': ['a', 'b', 'a', 'b', 'b']}), {'a': 2, 'b': 3})
