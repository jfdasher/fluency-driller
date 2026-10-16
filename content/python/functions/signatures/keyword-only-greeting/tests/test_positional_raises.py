def test_positional_raises():
    try:
        greet('Alice', 'Hello')
        assert False, 'Should have raised TypeError'
    except TypeError:
        pass
