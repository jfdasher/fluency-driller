def test_case_1():
    assert equal(sort_strings_by_vowel_count_then_alpha(**{'words': ['blue', 'red', 'green', 'ace', 'ox']}), ['ox', 'red', 'ace', 'blue', 'green'])
