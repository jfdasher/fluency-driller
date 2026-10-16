def test_case_2():
    assert equal(schedule_jobs(**{'jobs': [{'priority': 1, 'arrival': 1, 'name': 'solo'}]}), ['solo'])
