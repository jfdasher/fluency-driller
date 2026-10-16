def test_user_with_name():
    class User:
        def __init__(self, name):
            self.name = name
    assert get_username(User('alice')) == 'alice'
