def test_case_6():
    result = make_multiplier(**{'factor': 2})
    fn = make_multiplier
    assert result(2.5) == 5.0
