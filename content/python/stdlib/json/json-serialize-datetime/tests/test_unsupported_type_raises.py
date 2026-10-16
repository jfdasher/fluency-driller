def test_unsupported_type_raises():
    import json
    try:
        fn({'k': object()})
        assert False, 'Expected TypeError or ValueError'
    except (TypeError, ValueError):
        pass
