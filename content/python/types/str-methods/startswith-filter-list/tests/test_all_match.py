def test_all_match():
    result = filter_by_prefix(['test_a', 'test_b', 'test_c'], 'test_')
    assert result == ['test_a', 'test_b', 'test_c']
