def test_invalid_string_value_error():
    assert safe_parse('abc') is None
