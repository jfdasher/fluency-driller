def test_second_element_tiebreak():
    assert lex_sort([(1, 3), (1, 1), (1, 2)]) == [(1, 1), (1, 2), (1, 3)]
