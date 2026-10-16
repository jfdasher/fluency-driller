def test_case_2():
    assert equal(sort_tasks_by_priority(**{'tasks': [[1, 'only']]}), ['only'])
