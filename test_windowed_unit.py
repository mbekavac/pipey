from __future__ import annotations

import pytest

from windowed import WindowedIterable, dewindowify, windowify


def test_windowed_iterable_window_size_1() -> None:
    data = [0, 1, 2]
    result = list(WindowedIterable(data, 1))

    assert result == [
        ([], 0, [1]),
        ([0], 1, [2]),
        ([1], 2, []),
    ]


def test_windowed_iterable_window_size_2() -> None:
    data = [0, 1, 2, 3]
    result = list(WindowedIterable(data, 2))

    assert result == [
        ([], 0, [1, 2]),
        ([0], 1, [2, 3]),
        ([0, 1], 2, [3]),
        ([1, 2], 3, []),
    ]


def test_windowed_iterable_window_size_larger_than_data() -> None:
    data = [0, 1]
    result = list(WindowedIterable(data, 10))

    assert result == [
        ([], 0, [1]),
        ([0], 1, []),
    ]


def test_windowed_iterable_invalid_window_size() -> None:
    with pytest.raises(ValueError):
        WindowedIterable([1, 2, 3], 0)


def test_windowify_and_dewindowify_round_trip() -> None:
    data = [5, 6, 7]
    windowed = windowify(1)(data)
    assert list(dewindowify(windowed)) == data
