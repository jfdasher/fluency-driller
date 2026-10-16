def test_case_4():
    assert equal(count_items(**{'items': ['p', 'q', 'p', 'q', 'r']}), {'p': 2, 'q': 2, 'r': 1})
