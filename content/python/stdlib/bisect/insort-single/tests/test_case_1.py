def test_case_1():
    assert equal(insort_single(**{'sorted_list': [2, 4, 6], 'value': 1}), [1, 2, 4, 6])
