def test_case_0():
    assert equal(word_frequency(**{'words': ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']}), {'apple': 3, 'banana': 2, 'cherry': 1})
