def test_case_1():
    assert equal(exists_in_sorted(**{'sorted_list': [1, 3, 5, 7, 9], 'target': 4}), False)
