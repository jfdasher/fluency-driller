def test_case_2():
    assert equal(merge_dicts_unpack(**{'a': {}, 'b': {'m': 7}}), {'m': 7})
