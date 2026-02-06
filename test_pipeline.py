from __future__ import annotations

from collections import Counter
from typing import Iterable

from pipey import PipelineStep, apply_pipeline, modifier
from windowed import WindowedIterable, dewindowify, windowify


def simple_test_1() -> None:
    pipeline: list[PipelineStep] = [
        (lambda x: x*2, modifier.map),
        (lambda x: x > 5, modifier.filter),
        (lambda x: x - 1, modifier.map),
        (lambda x, y: x + y, modifier.reduce),
    ]

    assert apply_pipeline(range(10), pipeline) == 77


def simple_test_1_with_print() -> None:
    def foo1(x: int) -> int:
        print("Map 1")
        return x * 2

    def foo2(x: int) -> bool:
        print("Filter 1")
        return x > 5

    def foo3(x: int) -> int:
        print("Map 2")
        return x - 1

    def foo4(x: int, y: int) -> int:
        print("Reduce 1")
        return x + y

    pipeline: list[PipelineStep] = [
        (foo1, modifier.map),
        (foo2, modifier.filter),
        (foo3, modifier.map),
        (foo4, modifier.reduce),
    ]

    assert apply_pipeline(range(10), pipeline) == 77


def windowed_test_1() -> None:
    for element in WindowedIterable(range(10), 3):
        print(element)


def windowed_test_2() -> None:
    for element in WindowedIterable(range(10), 1):
        print(element)


def windowed_test_3() -> None:
    for element in WindowedIterable(range(5), 10):
        print(element)


def complex_test_1() -> None:
    pipeline: list[PipelineStep] = [
        (lambda x: x * 2, modifier.map),
        (windowify(2), modifier.window),
        (lambda x: sum(x[0]) > 4, modifier.filter),
        (dewindowify, modifier.window),
        (lambda x, y: x + y, modifier.reduce),
    ]

    assert apply_pipeline(range(10), pipeline) == 84


def complex_test_2() -> None:
    def foo1(counter: Counter[int], iterable: Iterable[int]) -> Counter[int]:
        counter.update(iterable)
        return counter

    pipeline: list[PipelineStep] = [
        (lambda x: x * 2, modifier.map),
        (foo1, modifier.reduce, Counter()),
    ]

    assert apply_pipeline([[1, 2, 3, 4], [1, 2, 3], [1, 2], [1]], pipeline) == Counter(
        {1: 8, 2: 6, 3: 4, 4: 2}
    )


def main() -> None:
    simple_test_1()
    simple_test_1_with_print()
    windowed_test_1()
    windowed_test_2()
    windowed_test_3()
    complex_test_1()
    complex_test_2()


if __name__ == "__main__":
    main()
