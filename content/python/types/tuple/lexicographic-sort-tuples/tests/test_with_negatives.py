def test_with_negatives():
    assert lex_sort([(-1, 2), (-2, 5), (0, 0)]) == [(-2, 5), (-1, 2), (0, 0)]
