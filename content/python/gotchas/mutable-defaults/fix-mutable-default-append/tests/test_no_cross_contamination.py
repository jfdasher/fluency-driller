def test_no_cross_contamination():
    for i in range(5):
        result = collect_items(i)
        assert result == [i], f'Call {i}: expected [{i}], got {result}'
