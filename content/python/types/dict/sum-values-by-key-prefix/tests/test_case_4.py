def test_case_4():
    assert equal(filter_a_keys(**{'d': {'a': 99}}), {'a': 99})
