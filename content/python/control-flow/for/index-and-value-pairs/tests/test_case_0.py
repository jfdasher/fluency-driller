def test_case_0():
    assert equal(index_and_value_pairs(**{'words': ['apple', 'banana', 'cherry']}), [[0, 'apple'], [1, 'banana'], [2, 'cherry']])
