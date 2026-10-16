def test_case_0():
    assert equal(filter_a_keys(**{'d': {'apple': 1, 'banana': 2, 'avocado': 3}}), {'apple': 1, 'avocado': 3})
