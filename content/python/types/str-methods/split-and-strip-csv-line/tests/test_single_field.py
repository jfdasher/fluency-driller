def test_single_field():
    assert parse_csv_line('  only  ') == ['only']
