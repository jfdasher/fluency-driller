def test_case_3():
    assert equal(invert_mapping(**{'mapping': {'sole': 99}}), {'99': 'sole'})
