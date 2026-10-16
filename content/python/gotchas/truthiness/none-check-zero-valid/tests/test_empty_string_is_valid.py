def test_empty_string_is_valid():
    assert get_value({'name': ''}, 'name', 'unknown') == ''
