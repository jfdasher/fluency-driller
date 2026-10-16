def test_case_1():
    assert equal(sum_tree(**{'root': {'val': 1, 'children': [{'val': 2, 'children': []}, {'val': 3, 'children': []}]}}), 6)
