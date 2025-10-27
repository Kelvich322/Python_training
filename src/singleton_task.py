# С помощью импорта:
from singleton import singleton

another_singleton = singleton
print(another_singleton is singleton)


# С помощью метакласса
class SingletonMeta(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self in SingletonMeta._instances:
            return SingletonMeta._instances[self]
        instance = super().__call__(*args, **kwargs)
        SingletonMeta._instances[self] = instance
        return instance


class MyMetaSingletonClass(metaclass=SingletonMeta):
    pass


obj1 = MyMetaSingletonClass()
obj2 = MyMetaSingletonClass()

print(obj1 is obj2)


# C помощью __new__ класса:
class Singleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


new_obj1 = Singleton()
new_obj2 = Singleton()

print(new_obj1 is new_obj2)
