def test_case_1():
    result = make_multiplier(**{'factor': 3})
    fn = make_multiplier
    assert result(0) == 0
