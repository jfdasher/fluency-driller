def test_number():
    assert json_round_trip(42) == 42
