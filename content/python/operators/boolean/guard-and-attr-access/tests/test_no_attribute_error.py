def test_no_attribute_error():
    try:
        result = get_username(None)
        assert result is None
    except AttributeError:
        assert False, 'AttributeError raised for None user'
