def test_case_2():
    assert equal(process_tasks(**{'tasks': ['x', 'y', 'z'], 'cancellations': []}), ['x', 'y', 'z'])
