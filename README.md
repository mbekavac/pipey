# pipey
## Simple processing pipeline mini-framework

Project layout:

- `src/pipey/`: library source
- `tests/`: unit tests
- `examples/`: runnable examples
- `benchmarks/`: benchmark scripts

Assuming your venv is activated and `python` points to it, run from project root:

```bash
python -m pip install -e ".[dev]"
```

Then run:

```bash
python examples/example.py
```

The example and benchmark scripts also work from a source checkout without installation.

Sample usage:

```python
from pipey import apply_pipeline, modifier

pipeline = [
    (lambda x: x*2, modifier.map),
    (lambda x: x > 5, modifier.filter),
    (lambda x: x - 1, modifier.map),
    (lambda x, y: x + y, modifier.reduce)
]

apply_pipeline(iter(range(0, 10)), pipeline)
```

Run the example:

```bash
python examples/example.py
```

Run tests:

```bash
python -m pytest
```

Benchmark:

```bash
python benchmarks/benchmark_pipeline.py
```

More complex real-word usage can be found at [my other repo](https://github.com/mbekavac/question_similarity_nlp_features/blob/master/extract_nlp_features.py).

Also comes with support for iterable caching and pre-fetching:

```python
from pipey import apply_pipeline, modifier
from pipey import WindowedIterable, dewindowify, windowify

pipeline = [
    (lambda x: x * 2, modifier.map),
    (windowify(2), modifier.window),
    (lambda x: sum(x[0]) > 4, modifier.filter),
    (dewindowify, modifier.window),
    (lambda x, y: x + y, modifier.reduce)
]

apply_pipeline(iter(range(0, 10)), pipeline)
```
