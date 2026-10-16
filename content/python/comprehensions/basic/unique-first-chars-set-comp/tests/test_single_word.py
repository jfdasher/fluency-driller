def test_single_word():
    result = unique_first_chars(['python'])
    assert result == {'p'}
