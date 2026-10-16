def test_case_4():
    result = slow_square(**{'n': 5})
    fn = slow_square
    assert hasattr(fn, 'cache_info')
