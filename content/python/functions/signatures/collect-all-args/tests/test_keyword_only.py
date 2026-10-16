def test_keyword_only():
    result = collect_args(x=10, y=20)
    assert result == ((), {'x': 10, 'y': 20})
