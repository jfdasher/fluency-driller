def test_case_5():
    result = make_multiplier(**{'factor': 1})
    fn = make_multiplier
    assert result(123) == 123
