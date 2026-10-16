def test_case_2():
    assert equal(collect_leaves(**{'root': {'val': 1, 'children': [{'val': 2, 'children': [{'val': 4, 'children': []}, {'val': 5, 'children': []}]}, {'val': 3, 'children': []}]}}), [4, 5, 3])
