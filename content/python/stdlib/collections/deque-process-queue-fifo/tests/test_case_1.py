def test_case_1():
    assert equal(process_tasks(**{'tasks': ['wash', 'cook', 'clean', 'cook'], 'cancellations': ['cook']}), ['wash', 'clean'])
