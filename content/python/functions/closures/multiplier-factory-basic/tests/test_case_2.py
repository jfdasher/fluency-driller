def test_case_2():
    result = make_multiplier(**{'factor': 7})
    fn = make_multiplier
    assert result(6) == 42
