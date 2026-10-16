def test_multi_char_sep():
    assert split_on_first('one::two::three', '::') == ('one', 'two::three')
