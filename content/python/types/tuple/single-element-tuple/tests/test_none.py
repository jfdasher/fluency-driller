def test_none():
    result = make_singleton(None)
    assert result == (None,)
    assert isinstance(result, tuple)
