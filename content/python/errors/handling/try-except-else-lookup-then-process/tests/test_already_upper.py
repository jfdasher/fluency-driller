def test_already_upper():
    assert get_processed({'k': 'HELLO'}, 'k') == 'HELLO'
