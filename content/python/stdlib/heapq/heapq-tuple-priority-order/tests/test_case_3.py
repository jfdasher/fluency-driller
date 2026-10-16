def test_case_3():
    assert equal(sort_tasks_by_priority(**{'tasks': [[2, 'second'], [2, 'also_second'], [1, 'first']]}), ['first', 'also_second', 'second'])
