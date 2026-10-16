def test_keyword_only_enforced():
    import inspect
    sig = inspect.signature(greet)
    p = sig.parameters['greeting']
    assert p.kind == inspect.Parameter.KEYWORD_ONLY
