def append_to_copy(data):
    copy = data[:]
    copy.append(99)
    return [data, copy]
