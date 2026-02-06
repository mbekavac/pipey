from __future__ import annotations

from collections.abc import Callable, Sequence
from enum import Enum
from functools import reduce
from typing import Any, TypeAlias


class Modifier(Enum):
    map = "map"
    filter = "filter"
    reduce = "reduce"
    window = "window"


modifier = Modifier

PipelineStep: TypeAlias = tuple[Callable[..., Any], Modifier, *tuple[Any, ...]]


def _apply_window(function_to_apply: Callable[..., Any], iterable: Any, *_: Any) -> Any:
    return function_to_apply(iterable)


_PIPELINE_FUNCTIONS: dict[Modifier, Callable[..., Any]] = {
    Modifier.map: map,
    Modifier.filter: filter,
    Modifier.reduce: reduce,
    Modifier.window: _apply_window,
}


def _validate_pipeline(pipeline: Sequence[PipelineStep]) -> None:
    for index, (_, function_type, *_) in enumerate(pipeline):
        if function_type is Modifier.reduce and index != len(pipeline) - 1:
            raise ValueError("Reduce step must be the last element in the pipeline.")


def apply_pipeline(
    input_iterable: Any,
    pipeline: Sequence[PipelineStep],
) -> Any:
    """
    Applies the pipeline to the input iterable.
    :param input_iterable: Input iterable.
    :param pipeline: List of pipeline elements, where each element is a tuple (function, pipey.modifier,
    *optional arguments).
    :return: Iterable over applied pipeline results.
    """
    _validate_pipeline(pipeline)

    pipeline_output: Any = input_iterable
    for function_to_apply, function_type, *optional_parameters in pipeline:
        pipeline_function = _PIPELINE_FUNCTIONS[function_type]
        pipeline_output = pipeline_function(function_to_apply, pipeline_output, *optional_parameters)

    return pipeline_output
