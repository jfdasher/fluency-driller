def test_list():
    lst = [1, 'hello', True, None]
    assert json_round_trip(lst) == lst
