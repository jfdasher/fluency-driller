def test_none_returns_default():
    assert get_value({'x': None}, 'x', 99) == 99
