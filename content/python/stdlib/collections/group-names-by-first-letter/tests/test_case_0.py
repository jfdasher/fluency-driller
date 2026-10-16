def test_case_0():
    assert equal(group_names_by_first_letter(**{'names': ['Alice', 'Bob', 'Anna', 'Brian', 'Charlie']}), {'A': ['Alice', 'Anna'], 'B': ['Bob', 'Brian'], 'C': ['Charlie']})
