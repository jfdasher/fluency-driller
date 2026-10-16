def test_mixed_args_and_kwargs():
    def greet(name, greeting='Hello'):
        return f'{greeting}, {name}!'
    assert logged_call(greet, 'Alice', greeting='Hi') == 'Hi, Alice!'
