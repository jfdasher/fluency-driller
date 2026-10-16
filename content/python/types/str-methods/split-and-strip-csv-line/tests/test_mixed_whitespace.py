def test_mixed_whitespace():
    assert parse_csv_line('  hello ,world  ,  foo  ') == ['hello', 'world', 'foo']
