def test_basic_colon():
    assert split_on_first('key:value', ':') == ('key', 'value')
