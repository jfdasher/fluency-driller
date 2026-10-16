def test_duplicates_collapsed():
    result = unique_first_chars(['sun', 'sand', 'sea', 'moon'])
    assert result == {'s', 'm'}
