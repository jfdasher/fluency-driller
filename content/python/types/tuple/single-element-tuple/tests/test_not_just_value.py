def test_not_just_value():
    result = make_singleton(7)
    assert result != 7
    assert isinstance(result, tuple)
