from __future__ import annotations

import argparse
import statistics
import time
from dataclasses import dataclass
from typing import Callable

from pipey import PipelineStep, apply_pipeline, modifier
from windowed import dewindowify, windowify


@dataclass(frozen=True)
class BenchmarkCase:
    name: str
    run: Callable[[int], int]
    expected: Callable[[int], int]


@dataclass(frozen=True)
class BenchmarkResult:
    name: str
    n: int
    avg_seconds: float
    min_seconds: float
    max_seconds: float
    stdev_seconds: float
    throughput_items_per_second: float


def _run_basic_pipeline(n: int) -> int:
    pipeline: list[PipelineStep] = [
        (lambda x: x * 2, modifier.map),
        (lambda x: x > 5, modifier.filter),
        (lambda x: x - 1, modifier.map),
        (lambda x, y: x + y, modifier.reduce),
    ]
    return apply_pipeline(range(n), pipeline)


def _expected_basic_pipeline(n: int) -> int:
    # Sum of (2i - 1) for i in [3, n-1].
    return (n - 3) * (n + 1)


def _run_windowed_pipeline(n: int) -> int:
    pipeline: list[PipelineStep] = [
        (lambda x: x * 2, modifier.map),
        (windowify(2), modifier.window),
        (lambda x: sum(x[0]) > 4, modifier.filter),
        (dewindowify, modifier.window),
        (lambda x, y: x + y, modifier.reduce),
    ]
    return apply_pipeline(range(n), pipeline)


def _expected_windowed_pipeline(n: int) -> int:
    # Sum of 2i for i in [3, n-1].
    return n * (n - 1) - 6


def _run_raw_windowed_only(n: int) -> int:
    return sum(current for _, current, _ in windowify(2)(range(n)))


def _expected_raw_windowed_only(n: int) -> int:
    return (n - 1) * n // 2


def _benchmark_case(case: BenchmarkCase, n: int, repeats: int, warmups: int) -> BenchmarkResult:
    for _ in range(warmups):
        result = case.run(n)
        if result != case.expected(n):
            raise AssertionError(f"{case.name}: unexpected warmup output {result}")

    durations_seconds: list[float] = []
    for _ in range(repeats):
        start = time.perf_counter()
        result = case.run(n)
        duration_seconds = time.perf_counter() - start
        if result != case.expected(n):
            raise AssertionError(f"{case.name}: unexpected output {result}")
        durations_seconds.append(duration_seconds)

    avg_seconds = statistics.mean(durations_seconds)
    min_seconds = min(durations_seconds)
    max_seconds = max(durations_seconds)
    stdev_seconds = statistics.stdev(durations_seconds) if len(durations_seconds) > 1 else 0.0
    throughput_items_per_second = n / avg_seconds if avg_seconds > 0 else float("inf")

    return BenchmarkResult(
        name=case.name,
        n=n,
        avg_seconds=avg_seconds,
        min_seconds=min_seconds,
        max_seconds=max_seconds,
        stdev_seconds=stdev_seconds,
        throughput_items_per_second=throughput_items_per_second,
    )


def _print_results(results: list[BenchmarkResult]) -> None:
    print()
    print("Benchmark Results")
    print(
        f"{'case':<25} {'n':>10} {'avg (s)':>12} {'min (s)':>12} "
        f"{'max (s)':>12} {'stdev (s)':>12} {'items/s':>14}"
    )
    print("-" * 100)
    for result in results:
        print(
            f"{result.name:<25} {result.n:>10} {result.avg_seconds:>12.6f} {result.min_seconds:>12.6f} "
            f"{result.max_seconds:>12.6f} {result.stdev_seconds:>12.6f} {result.throughput_items_per_second:>14.0f}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark pipey/windowed execution speed.")
    parser.add_argument("--n", type=int, default=200_000, help="Number of input items (must be >= 4).")
    parser.add_argument("--repeats", type=int, default=7, help="Measured runs per case.")
    parser.add_argument("--warmups", type=int, default=2, help="Warmup runs per case.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.n < 4:
        raise ValueError("--n must be >= 4 so reduce pipelines have non-empty inputs.")
    if args.repeats < 1:
        raise ValueError("--repeats must be >= 1")
    if args.warmups < 0:
        raise ValueError("--warmups must be >= 0")

    cases = [
        BenchmarkCase("basic_pipeline", _run_basic_pipeline, _expected_basic_pipeline),
        BenchmarkCase("windowed_pipeline", _run_windowed_pipeline, _expected_windowed_pipeline),
        BenchmarkCase("windowed_only_sum", _run_raw_windowed_only, _expected_raw_windowed_only),
    ]
    results = [_benchmark_case(case, args.n, args.repeats, args.warmups) for case in cases]
    _print_results(results)


if __name__ == "__main__":
    main()
