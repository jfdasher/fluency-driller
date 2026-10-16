def test_sep_at_start():
    assert split_on_first(':value', ':') == ('', 'value')
