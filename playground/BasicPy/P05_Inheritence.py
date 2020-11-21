class A(object):
    countA = 11

    def __init__(self):
        pass

    def foo(self):
        print('A foo')


class B(object):
    countB = 12

    def __init__(self):
        pass

    def foo(self):
        print('B foo')


class C(B, A):

    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        pass


if __name__ == '__main__':
    testc = C()
    print(testc.foo())
    print(C.countA)
    print(C.countB)
    # print(C.countC)
