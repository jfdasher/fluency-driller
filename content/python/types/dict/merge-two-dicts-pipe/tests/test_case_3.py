def test_case_3():
    assert equal(merge_dicts_pipe(**{'a': {'k': 1}, 'b': {}}), {'k': 1})
