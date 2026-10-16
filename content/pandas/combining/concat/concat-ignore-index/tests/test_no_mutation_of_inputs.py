def test_no_mutation_of_inputs():
    import pandas as pd
    top = pd.DataFrame({'name': ['Alice', 'Bob'], 'score': [85, 90]})
    bottom = pd.DataFrame({'name': ['Carol', 'Dave'], 'score': [78, 92]})
    top_copy = top.copy()
    bottom_copy = bottom.copy()
    fn(top, bottom)
    from pandas.testing import assert_frame_equal
    assert_frame_equal(top, top_copy)
    assert_frame_equal(bottom, bottom_copy)
