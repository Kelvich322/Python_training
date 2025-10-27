class _MySingletonClass:
    def __init__(self, data):
        self.data = data


singleton = _MySingletonClass(data="some data")
