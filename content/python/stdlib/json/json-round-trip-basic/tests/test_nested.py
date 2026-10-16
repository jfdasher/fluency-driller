def test_nested():
    obj = {'x': {'y': [1, 2, {'z': 3}]}}
    assert json_round_trip(obj) == obj
