def test_case_4():
    assert equal(value_to_index(**{'items': ['cat', 'dog', 'bird', 'fish']}), {'cat': 0, 'dog': 1, 'bird': 2, 'fish': 3})
