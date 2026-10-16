def test_equal_value_strings():
    a = 'hello'
    b = 'hel' + 'lo'
    assert equal_value(a, b) == True
