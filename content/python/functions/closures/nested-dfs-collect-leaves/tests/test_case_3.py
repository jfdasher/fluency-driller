def test_case_3():
    assert equal(collect_leaves(**{'root': {'val': 9, 'children': [{'val': 7, 'children': [{'val': 3, 'children': [{'val': 1, 'children': []}]}]}]}}), [1])
