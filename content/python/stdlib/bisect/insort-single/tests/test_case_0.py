def test_case_0():
    assert equal(insort_single(**{'sorted_list': [1, 3, 5, 7], 'value': 4}), [1, 3, 4, 5, 7])
