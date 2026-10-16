def test_case_4():
    assert equal(count_distinct(**{'words': ['x', 'y', 'x', 'z', 'y', 'z']}), 3)
