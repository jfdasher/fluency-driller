def test_case_1():
    assert equal(merge_dicts_pipe(**{'a': {'name': 'Alice'}, 'b': {'age': 30}}), {'name': 'Alice', 'age': 30})
