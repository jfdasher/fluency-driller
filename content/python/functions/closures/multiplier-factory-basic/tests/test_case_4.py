def test_case_4():
    result = make_multiplier(**{'factor': 0})
    fn = make_multiplier
    assert result(99) == 0
