def test_empty_prefix():
    result = filter_by_prefix(['hello', 'world'], '')
    assert result == ['hello', 'world']
