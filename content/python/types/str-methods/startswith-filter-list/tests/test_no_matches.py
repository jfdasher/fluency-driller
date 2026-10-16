def test_no_matches():
    result = filter_by_prefix(['cat', 'dog', 'fish'], 'z')
    assert result == []
