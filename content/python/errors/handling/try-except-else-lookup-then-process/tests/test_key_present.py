def test_key_present():
    assert get_processed({'name': 'alice'}, 'name') == 'ALICE'
