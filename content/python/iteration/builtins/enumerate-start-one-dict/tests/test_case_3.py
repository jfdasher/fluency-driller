def test_case_3():
    assert equal(index_from_one(**{'items': ['red', 'green', 'blue']}), {'1': 'red', '2': 'green', '3': 'blue'})
