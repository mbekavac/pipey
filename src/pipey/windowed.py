from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable, Iterator
from typing import Self, TypeAlias, TypeVar

T = TypeVar("T")
WindowView: TypeAlias = tuple[list[T], T, list[T]]


class WindowedIterable(Iterator[WindowView[T]]):
    """
    Iterator that yields:
    - values to the left of the current element (up to ``window_size``),
    - the current element,
    - values to the right of the current element (up to ``window_size``).
    """

    def __init__(self, iterable: Iterable[T], window_size: int) -> None:
        if window_size < 1:
            raise ValueError("window_size must be >= 1")

        self._source: Iterator[T] = iter(iterable)
        self._window_size = window_size
        self._left_window: deque[T] = deque(maxlen=window_size)
        self._right_window: deque[T] = deque()
        self._fill_right_window()

    def _fill_right_window(self) -> None:
        while len(self._right_window) < self._window_size:
            try:
                self._right_window.append(next(self._source))
            except StopIteration:
                return

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> WindowView[T]:
        if not self._right_window:
            raise StopIteration

        current = self._right_window.popleft()
        self._fill_right_window()

        # Snapshot before recording current as part of the left window for the next step.
        windowed_value = (list(self._left_window), current, list(self._right_window))
        self._left_window.append(current)
        return windowed_value


def windowify(window_size: int) -> Callable[[Iterable[T]], WindowedIterable[T]]:
    """
    Factory function for transforming any iterable to a WindowedIterable. Can be used as a function in pipey pipeline.
    :param window_size: Number of cached elements to the left and right of the current element.
    :return: Function that takes an iterable as input and outputs the corresponding WindowedIterable.
    """
    def windowed(iterable: Iterable[T]) -> WindowedIterable[T]:
        return WindowedIterable(iterable, window_size)

    return windowed


def dewindowify(iterable: Iterable[WindowView[T]]) -> Iterator[T]:
    """
    Yields elements from a WindowedIterable without the cached windows. Can be used as a function in pipey pipeline.
    :param iterable: WindowedIterable to be transformed.
    :return: None.
    """
    for _, current, _ in iterable:
        yield current
