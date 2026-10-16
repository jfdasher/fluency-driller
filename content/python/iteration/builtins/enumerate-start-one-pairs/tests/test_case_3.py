def test_case_3():
    assert equal(number_items(**{'items': ['cat', 'dog', 'bird', 'fish']}), [[1, 'cat'], [2, 'dog'], [3, 'bird'], [4, 'fish']])
