def test_case_3():
    assert equal(index_and_value_pairs(**{'words': ['hello', 'world']}), [[0, 'hello'], [1, 'world']])
