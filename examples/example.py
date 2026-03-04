from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, TypeAlias

# Allow running directly from a source checkout without editable install.
ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from pipey import apply_pipeline, dewindowify, modifier, windowify

PipelineStep: TypeAlias = (
    tuple[Callable[..., Any], modifier]
    | tuple[Callable[..., Any], modifier, Any]
)


def basic_example() -> None:
    print("basic_example steps:")
    print("1. map: x * 2")
    print("2. filter: x > 5")
    print("3. map: x - 1")
    print("4. reduce: sum")
    print("Input: range(0, 10)")
    print("Expected output: 77")

    pipeline: list[PipelineStep] = [
        (lambda x: x * 2, modifier.map),
        (lambda x: x > 5, modifier.filter),
        (lambda x: x - 1, modifier.map),
        (lambda x, y: x + y, modifier.reduce),
    ]

    result: int = apply_pipeline(range(10), pipeline)
    print(f"basic_example result: {result}")


def windowed_example() -> None:
    print("windowed_example steps:")
    print("1. map: x * 2")
    print("2. window: windowify(2) -> (previous, current, next)")
    print("3. filter: sum(previous) > 4")
    print("4. window: dewindowify -> current only")
    print("5. reduce: sum")
    print("Input: range(0, 10)")
    print("Expected output: 84")

    pipeline: list[PipelineStep] = [
        (lambda x: x * 2, modifier.map),
        (windowify(2), modifier.window),
        (lambda x: sum(x[0]) > 4, modifier.filter),
        (dewindowify, modifier.window),
        (lambda x, y: x + y, modifier.reduce),
    ]

    result: int = apply_pipeline(range(10), pipeline)
    print(f"windowed_example result: {result}")


if __name__ == "__main__":
    basic_example()
    windowed_example()
