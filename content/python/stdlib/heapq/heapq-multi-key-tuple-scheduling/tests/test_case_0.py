def test_case_0():
    assert equal(schedule_jobs(**{'jobs': [{'priority': 2, 'arrival': 1, 'name': 'B'}, {'priority': 1, 'arrival': 3, 'name': 'C'}, {'priority': 1, 'arrival': 1, 'name': 'A'}]}), ['A', 'C', 'B'])
