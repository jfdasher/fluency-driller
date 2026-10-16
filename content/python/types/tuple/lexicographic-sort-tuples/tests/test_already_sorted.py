def test_already_sorted():
    assert lex_sort([(1, 0), (2, 0), (3, 0)]) == [(1, 0), (2, 0), (3, 0)]
