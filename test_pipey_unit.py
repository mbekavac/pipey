import pytest

from pipey import apply_pipeline, modifier


def test_apply_pipeline_basic_map_filter_reduce():
    pipeline = [
        (lambda x: x * 2, modifier.map),
        (lambda x: x > 5, modifier.filter),
        (lambda x: x - 1, modifier.map),
        (lambda x, y: x + y, modifier.reduce),
    ]

    assert apply_pipeline(range(10), pipeline) == 77


def test_apply_pipeline_reduce_must_be_last():
    pipeline = [
        (lambda x: x + 1, modifier.map),
        (lambda x, y: x + y, modifier.reduce),
        (lambda x: x * 2, modifier.map),
    ]

    with pytest.raises(AssertionError):
        apply_pipeline(range(5), pipeline)


def test_apply_pipeline_reduce_with_initial_value():
    pipeline = [
        (lambda x: x + 1, modifier.map),
        (lambda acc, x: acc + x, modifier.reduce, 10),
    ]

    assert apply_pipeline(range(3), pipeline) == 16


def test_apply_pipeline_window_passthrough():
    def add_marker(iterable):
        for item in iterable:
            yield ("x", item)

    pipeline = [
        (add_marker, modifier.window),
        (lambda t: t[1], modifier.map),
        (lambda x, y: x + y, modifier.reduce),
    ]

    assert apply_pipeline(range(4), pipeline) == 6


def test_modifier_members():
    assert modifier.map.name == "map"
    assert modifier.filter.name == "filter"
    assert modifier.reduce.name == "reduce"
    assert modifier.window.name == "window"
