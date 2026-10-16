def test_case_1():
    assert equal(sort_tasks_by_priority(**{'tasks': [[5, 'e'], [1, 'a'], [3, 'c'], [2, 'b'], [4, 'd']]}), ['a', 'b', 'c', 'd', 'e'])
