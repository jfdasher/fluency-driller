def test_case_1():
    assert equal(schedule_jobs(**{'jobs': [{'priority': 3, 'arrival': 1, 'name': 'X'}, {'priority': 1, 'arrival': 5, 'name': 'Y'}, {'priority': 2, 'arrival': 2, 'name': 'Z'}, {'priority': 1, 'arrival': 2, 'name': 'W'}]}), ['W', 'Y', 'Z', 'X'])
