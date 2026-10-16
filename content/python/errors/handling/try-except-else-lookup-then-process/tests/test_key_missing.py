def test_key_missing():
    assert get_processed({'name': 'alice'}, 'age') is None
