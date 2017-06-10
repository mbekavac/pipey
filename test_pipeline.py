from pipey import apply_pipeline, modifier
from windowed import WindowedIterable, windowify, dewindowify


def simple_test_1():
    p = [
        (lambda x: x*2, modifier.map),
        (lambda x: x > 5, modifier.filter),
        (lambda x: x - 1, modifier.map),
        (lambda x, y: x + y, modifier.reduce)
    ]

    assert apply_pipeline(iter(range(0, 10)), p) == 77


def simple_test_1_with_print():
    def foo1(x):
        print('Map 1')
        return x*2

    def foo2(x):
        print('Filter 1')
        return x > 5

    def foo3(x):
        print('Map 2')
        return x - 1

    def foo4(x, y):
        print('Reduce 1')
        return x + y

    p = [
        (foo1, modifier.map),
        (foo2, modifier.filter),
        (foo3, modifier.map),
        (foo4, modifier.reduce)
    ]

    assert apply_pipeline(iter(range(0, 10)), p) == 77


def windowed_test_1():
    for element in WindowedIterable(range(0, 10), 3):
        print(element)


def windowed_test_2():
    for element in WindowedIterable(range(0, 10), 1):
        print(element)


def windowed_test_3():
    for element in WindowedIterable(range(0, 5), 10):
        print(element)


def complex_test_1():
    p = [
        (lambda x: x * 2, modifier.map),
        (windowify(2), modifier.window),
        (lambda x: sum(x[0]) > 4, modifier.filter),
        (dewindowify, modifier.window),
        (lambda x, y: x + y, modifier.reduce)
    ]

    assert apply_pipeline(iter(range(0, 10)), p) == 84


def complex_test_2():
    from collections import Counter

    def foo1(counter, iterable):
        counter.update(iterable)
        return counter

    p = [
        (lambda x: x * 2, modifier.map),
        (foo1, modifier.reduce, Counter())
    ]

    assert apply_pipeline([[1, 2, 3, 4], [1, 2, 3], [1, 2], [1]], p) == Counter({1: 8, 2: 6, 3: 4, 4: 2})


simple_test_1()
simple_test_1_with_print()
windowed_test_1()
windowed_test_2()
windowed_test_3()
complex_test_1()
complex_test_2()
