def test_empty_fields():
    assert parse_csv_line('a,,b') == ['a', '', 'b']
