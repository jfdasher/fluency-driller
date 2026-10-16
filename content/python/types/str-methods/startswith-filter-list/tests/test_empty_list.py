def test_empty_list():
    result = filter_by_prefix([], 'pre')
    assert result == []
