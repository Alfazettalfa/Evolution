class A():
    def __init__(self):
        self.x = 1
    def d(self):
        del self

b = A()
l = [1, 2, A(), b, 5]
print(l)
del b
print(l)