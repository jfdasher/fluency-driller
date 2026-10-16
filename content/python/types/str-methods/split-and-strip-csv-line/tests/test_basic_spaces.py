def test_basic_spaces():
    assert parse_csv_line('a , b , c') == ['a', 'b', 'c']
