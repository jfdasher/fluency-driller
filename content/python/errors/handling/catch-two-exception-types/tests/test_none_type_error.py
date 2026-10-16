def test_none_type_error():
    assert safe_parse(None) is None
