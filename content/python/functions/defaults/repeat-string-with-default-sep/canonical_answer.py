def repeat_str(text, times=3, sep='-'):
    return sep.join([text] * times)

def call_with_dot():
    return repeat_str('ab', sep='.')
