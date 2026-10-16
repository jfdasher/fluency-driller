def test_return_value_preserved():
    assert logged_call(sum, [10, 20, 30]) == 60
