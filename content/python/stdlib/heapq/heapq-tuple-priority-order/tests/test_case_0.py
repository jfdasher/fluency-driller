def test_case_0():
    assert equal(sort_tasks_by_priority(**{'tasks': [[3, 'low'], [1, 'high'], [2, 'medium']]}), ['high', 'medium', 'low'])
