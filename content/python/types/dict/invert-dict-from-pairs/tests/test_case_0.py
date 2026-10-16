def test_case_0():
    assert equal(invert_mapping(**{'mapping': {'apple': 1, 'banana': 2, 'cherry': 3}}), {'1': 'apple', '2': 'banana', '3': 'cherry'})
