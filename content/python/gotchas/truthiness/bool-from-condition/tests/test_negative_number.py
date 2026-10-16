def test_negative_number():
    assert is_positive(-3) == False
    assert type(is_positive(-3)) is bool
