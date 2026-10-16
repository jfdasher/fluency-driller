def test_case_3():
    assert equal(schedule_jobs(**{'jobs': [{'priority': 2, 'arrival': 2, 'name': 'D'}, {'priority': 2, 'arrival': 1, 'name': 'C'}, {'priority': 1, 'arrival': 2, 'name': 'B'}, {'priority': 1, 'arrival': 1, 'name': 'A'}]}), ['A', 'B', 'C', 'D'])
