def test_case_4():
    assert equal(process_tasks(**{'tasks': [], 'cancellations': ['a']}), [])
