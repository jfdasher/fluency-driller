def test_case_0():
    assert equal(sort_people_by_age_then_name(**{'people': [['Alice', 30], ['Bob', 25], ['Carol', 30], ['Dave', 25]]}), [['Bob', 25], ['Dave', 25], ['Alice', 30], ['Carol', 30]])
