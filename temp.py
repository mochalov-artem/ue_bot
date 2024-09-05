from pympler import asizeof


class Test1:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @staticmethod
    def test(a: int):
        return f'test static method {a}'


class Test2:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def test(a: int):
        return f'test static method {a}'


print(asizeof.asizeof(Test1(1, 2)))
print(asizeof.asizeof(Test2(1, 2)))
