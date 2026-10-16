def test_case_0():
    assert equal(process_tasks(**{'tasks': ['a', 'b', 'c', 'd'], 'cancellations': ['b', 'd']}), ['a', 'c'])
