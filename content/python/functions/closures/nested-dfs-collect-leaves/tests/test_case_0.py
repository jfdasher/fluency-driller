def test_case_0():
    assert equal(collect_leaves(**{'root': {'val': 1, 'children': []}}), [1])
