class Widget:
    count = 0

    def __init__(self):
        Widget.count += 1

    @classmethod
    def get_count(cls):
        return cls.count
