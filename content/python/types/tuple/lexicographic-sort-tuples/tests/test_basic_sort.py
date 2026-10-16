def test_basic_sort():
    assert lex_sort([(3, 1), (1, 5), (2, 0)]) == [(1, 5), (2, 0), (3, 1)]
