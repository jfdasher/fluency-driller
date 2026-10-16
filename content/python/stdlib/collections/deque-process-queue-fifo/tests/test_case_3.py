def test_case_3():
    assert equal(process_tasks(**{'tasks': ['a', 'b', 'c'], 'cancellations': ['a', 'b', 'c']}), [])
