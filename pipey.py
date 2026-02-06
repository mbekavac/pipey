from __future__ import annotations

from enum import Enum
from functools import reduce
from typing import Any, Callable, TypeAlias


class Modifier(Enum):
    map = "map"
    filter = "filter"
    reduce = "reduce"
    window = "window"


modifier = Modifier

PipelineStep: TypeAlias = (
    tuple[Callable[..., Any], Modifier]
    | tuple[Callable[..., Any], Modifier, Any]
)

__pipeline_functions: dict[Modifier, Callable[..., Any]] = {
    Modifier.map: map,
    Modifier.filter: filter,
    Modifier.reduce: reduce,
    Modifier.window: lambda f, x: f(x),
}


def __apply_pipeline(
    input_iterable: Any,
    pipeline: list[PipelineStep],
) -> Any:
    if not pipeline:
        return input_iterable

    function_to_apply, function_type, *optional_parameters = pipeline.pop(0)
    assert len(pipeline) == 0 or function_type is not Modifier.reduce

    applied_function = __pipeline_functions[function_type](
        function_to_apply,
        input_iterable,
        *optional_parameters,
    )
    return __apply_pipeline(applied_function, pipeline)


def apply_pipeline(
    input_iterable: Any,
    pipeline: list[PipelineStep],
) -> Any:
    """
    Applies the pipeline to the input iterable.
    :param input_iterable: Input iterable.
    :param pipeline: List of pipeline elements, where each element is a tuple (function, pipey.modifier,
    *optional arguments).
    :return: Iterable over applied pipeline results.
    """
    pipeline_copy = pipeline[:]
    return __apply_pipeline(input_iterable, pipeline_copy)
