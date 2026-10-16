def test_positional_only():
    result = collect_args(1, 2, 3)
    assert result == ((1, 2, 3), {})
