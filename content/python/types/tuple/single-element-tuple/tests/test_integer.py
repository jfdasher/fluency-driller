def test_integer():
    result = make_singleton(42)
    assert result == (42,)
    assert isinstance(result, tuple)
    assert len(result) == 1
