def test_string():
    result = make_singleton('hello')
    assert result == ('hello',)
    assert isinstance(result, tuple)
    assert len(result) == 1
