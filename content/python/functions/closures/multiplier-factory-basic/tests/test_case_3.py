def test_case_3():
    result = make_multiplier(**{'factor': -2})
    fn = make_multiplier
    assert result(4) == -8
