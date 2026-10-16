def test_fresh_list_each_call():
    result1 = collect_items(1)
    result2 = collect_items(2)
    assert result1 == [1], f'Expected [1], got {result1}'
    assert result2 == [2], f'Expected [2], got {result2}'
