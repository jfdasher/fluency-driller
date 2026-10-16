def test_case_1():
    assert equal(sorted_copy(**{'lst': [5, 4, 3, 2, 1]}), [1, 2, 3, 4, 5])
