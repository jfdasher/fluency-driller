def test_no_spaces():
    assert parse_csv_line('one,two,three') == ['one', 'two', 'three']
