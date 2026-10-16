def test_explicit_list_shared():
    shared = []
    collect_items(10, shared)
    collect_items(20, shared)
    assert shared == [10, 20]
