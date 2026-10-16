def test_list_type_error():
    assert safe_parse([1, 2]) is None
