def test_case_3():
    assert equal(sum_tree(**{'root': {'val': 0, 'children': [{'val': 0, 'children': [{'val': 0, 'children': []}]}]}}), 0)
