from enum import Enum
from functools import reduce

modifier = Enum('modifier', 'map filter reduce window')


__pipeline_functions = {
    modifier.map: map,
    modifier.filter: filter,
    modifier.reduce: reduce,
    modifier.window: lambda f, x: f(x)
}


def __apply_pipeline(input_iterable, pipeline):
    if len(pipeline) == 0:
        return input_iterable

    function_to_apply, function_type, *optional_parameters = pipeline.pop(0)
    assert len(pipeline) == 0 or function_type != modifier.reduce

    applied_function = __pipeline_functions[function_type](function_to_apply, input_iterable, *optional_parameters)
    return __apply_pipeline(applied_function, pipeline)


def apply_pipeline(input_iterable, pipeline):
    """
    Applies the pipeline to the input iterable.
    :param input_iterable: Input iterable.
    :param pipeline: List of pipeline elements, where each element is a tuple (function, pipey.modifier,
    *optional arguments).
    :return: Iterable over applied pipeline results.
    """
    pipeline_copy = pipeline[:]
    return __apply_pipeline(input_iterable, pipeline_copy)
