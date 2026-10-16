def test_case_1():
    assert equal(collect_leaves(**{'root': {'val': 1, 'children': [{'val': 2, 'children': []}, {'val': 3, 'children': []}]}}), [2, 3])
