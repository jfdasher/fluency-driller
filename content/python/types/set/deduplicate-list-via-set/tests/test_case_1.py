def test_case_1():
    assert equal(deduplicate_list(**{'nums': [5, 5, 5, 5]}), [5])
