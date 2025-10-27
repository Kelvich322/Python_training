from datetime import datetime


class CreatedMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs["created_at"] = datetime.now()
        return super().__new__(cls, name, bases, attrs)


class A(metaclass=CreatedMeta):
    pass


obj = A()
print(obj.created_at)
