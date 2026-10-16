def test_different_name():
    class User:
        def __init__(self, name):
            self.name = name
    assert get_username(User('bob')) == 'bob'
