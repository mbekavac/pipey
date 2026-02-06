from pipey import apply_pipeline, modifier
from windowed import windowify, dewindowify


def basic_example():
    print("basic_example steps:")
    print("1. map: x * 2")
    print("2. filter: x > 5")
    print("3. map: x - 1")
    print("4. reduce: sum")
    print("Input: range(0, 10)")
    print("Expected output: 77")

    pipeline = [
        (lambda x: x * 2, modifier.map),
        (lambda x: x > 5, modifier.filter),
        (lambda x: x - 1, modifier.map),
        (lambda x, y: x + y, modifier.reduce),
    ]

    result = apply_pipeline(iter(range(0, 10)), pipeline)
    print("basic_example result:", result)


def windowed_example():
    print("windowed_example steps:")
    print("1. map: x * 2")
    print("2. window: windowify(2) -> (previous, current, next)")
    print("3. filter: sum(previous) > 4")
    print("4. window: dewindowify -> current only")
    print("5. reduce: sum")
    print("Input: range(0, 10)")
    print("Expected output: 84")

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
