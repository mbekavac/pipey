from pipey import apply_pipeline, modifier
from windowed import windowify, dewindowify


def basic_example():
    pipeline = [
        (lambda x: x * 2, modifier.map),
        (lambda x: x > 5, modifier.filter),
        (lambda x: x - 1, modifier.map),
        (lambda x, y: x + y, modifier.reduce),
    ]

    result = apply_pipeline(iter(range(0, 10)), pipeline)
    print("basic_example result:", result)


def windowed_example():
    pipeline = [
        (lambda x: x * 2, modifier.map),
        (windowify(2), modifier.window),
        (lambda x: sum(x[0]) > 4, modifier.filter),
        (dewindowify, modifier.window),
        (lambda x, y: x + y, modifier.reduce),
    ]

    result = apply_pipeline(iter(range(0, 10)), pipeline)
    print("windowed_example result:", result)


if __name__ == "__main__":
    basic_example()
    windowed_example()
