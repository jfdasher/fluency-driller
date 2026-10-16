def test_positional_only():
    result = logged_call(max, 3, 1, 2)
    assert result == 3
