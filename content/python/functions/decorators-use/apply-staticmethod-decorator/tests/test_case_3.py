def test_case_3():
    result = MathUtils(**{})
    fn = MathUtils
    assert isinstance(result.__class__.__dict__['add'], staticmethod)
