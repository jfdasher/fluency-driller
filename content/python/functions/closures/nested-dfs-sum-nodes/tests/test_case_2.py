def test_case_2():
    assert equal(sum_tree(**{'root': {'val': 5, 'children': [{'val': 3, 'children': [{'val': 1, 'children': []}, {'val': 2, 'children': []}]}, {'val': 4, 'children': []}]}}), 15)
