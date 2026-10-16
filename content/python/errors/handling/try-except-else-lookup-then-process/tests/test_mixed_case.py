def test_mixed_case():
    assert get_processed({'city': 'Paris'}, 'city') == 'PARIS'
