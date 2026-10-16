def test_case_0():
    assert equal(merge_dicts_unpack(**{'a': {'x': 1, 'y': 2}, 'b': {'y': 3, 'z': 4}}), {'x': 1, 'y': 3, 'z': 4})
