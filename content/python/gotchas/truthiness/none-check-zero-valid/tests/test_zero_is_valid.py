def test_zero_is_valid():
    assert get_value({'count': 0}, 'count', 42) == 0
