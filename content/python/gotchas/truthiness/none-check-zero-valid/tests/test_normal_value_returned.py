def test_normal_value_returned():
    assert get_value({'a': 5}, 'a', 0) == 5
