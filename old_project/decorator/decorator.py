def outer(fn):
    def inner():
        print('记录日志开始')
        fn()
        print('记录日志结束')
    return inner

def foo():
    print("it is foo ")

foo = outer(foo)
foo()