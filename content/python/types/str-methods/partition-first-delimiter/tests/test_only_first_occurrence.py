def test_only_first_occurrence():
    assert split_on_first('a:b:c', ':') == ('a', 'b:c')
