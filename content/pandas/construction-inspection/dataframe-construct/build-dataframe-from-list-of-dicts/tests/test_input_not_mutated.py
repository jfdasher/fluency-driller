def test_input_not_mutated():
    records = [
        {"x": 1, "y": 2},
        {"x": 3, "y": 4},
    ]
    original = [dict(r) for r in records]
    fn(records)
    assert records == original, "Input list of dicts was mutated"
