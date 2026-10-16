def uppercase(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

def bold(func):
    def wrapper(*args, **kwargs):
        return f'**{func(*args, **kwargs)}**'
    return wrapper

@bold
@uppercase
def greet(name):
    return 'hello ' + name
