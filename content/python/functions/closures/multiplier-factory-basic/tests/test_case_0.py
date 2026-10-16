def test_case_0():
    result = make_multiplier(**{'factor': 3})
    fn = make_multiplier
    assert result(5) == 15
