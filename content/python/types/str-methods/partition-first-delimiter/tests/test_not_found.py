def test_not_found():
    assert split_on_first('hello', ':') == ('hello', '')
