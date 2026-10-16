def test_case_1():
    assert equal(invert_mapping(**{'mapping': {'red': 10, 'green': 20, 'blue': 30}}), {'10': 'red', '20': 'green', '30': 'blue'})
