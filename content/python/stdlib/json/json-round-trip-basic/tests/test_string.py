def test_string():
    assert json_round_trip('hello world') == 'hello world'
