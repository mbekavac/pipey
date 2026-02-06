from __future__ import annotations

from typing import Callable, Iterable, Iterator, Optional, Self, TypeVar

T = TypeVar("T")


class WindowedIterable(Iterator[tuple[list[T], T, list[T]]]):
    """
    Iterable with an additional capability of looking back or ahead within a specified window size.
    Each iteration step yields the window before the current element, the current element and the window after the
    current element.
    """

    def __init__(self, iterable: Iterable[T], window_size: int) -> None:
        if window_size < 1:
            raise ValueError("window_size must be >= 1")
        self._iterable: Iterator[T] = iter(iterable)
        self._previous: list[T] = []
        self._current: Optional[T] = None
        self._next: list[T] = []
        self._window_size = window_size
        self._is_current_set = False

        self.__get_next(window_size)

    def __get_next(self, number_of_elements: int) -> None:
        for _ in range(number_of_elements):
            try:
                self._next.append(next(self._iterable))
            except StopIteration:
                return

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> tuple[list[T], T, list[T]]:
        if not self._next:
            raise StopIteration

        if self._is_current_set and self._current is not None:
            self._previous.append(self._current)

        current = self._next[0]
        self._current = current
        self._is_current_set = True

        self._next.pop(0)
        self.__get_next(1)

        if len(self._previous) > self._window_size:
            self._previous.pop(0)

        return self._previous[:], current, self._next[:]


def windowify(window_size: int) -> Callable[[Iterable[T]], WindowedIterable[T]]:
    """
    Factory function for transforming any iterable to a WindowedIterable. Can be used as a function in pipey pipeline.
    :param window_size: Number of cached elements to the left and right of the current element.
    :return: Function that takes an iterable as input and outputs the corresponding WindowedIterable.
    """
    def windowed(iterable: Iterable[T]) -> WindowedIterable[T]:
        return WindowedIterable(iterable, window_size)
    return windowed


def dewindowify(iterable: Iterable[tuple[list[T], T, list[T]]]) -> Iterator[T]:
    """
    Yields elements from a WindowedIterable without the cached windows. Can be used as a function in pipey pipeline.
    :param iterable: WindowedIterable to be transformed.
    :return: None.
    """
    for _, current, _ in iterable:
        yield current
