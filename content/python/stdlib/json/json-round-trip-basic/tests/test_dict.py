def test_dict():
    d = {'a': 1, 'b': [2, 3]}
    assert json_round_trip(d) == d
