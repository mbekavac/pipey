# pipey
## Simple processing pipeline mini-framework

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

More complex real-word usage can be found at [my other repo](https://github.com/mbekavac/question_similarity_nlp_features/blob/master/extract_nlp_features.py).

Also comes with support for iterable caching and pre-fetching:

```python
from pipey import apply_pipeline, modifier
from windowed import WindowedIterable, windowify, dewindowify

pipeline = [
    (lambda x: x * 2, modifier.map),
    (windowify(2), modifier.window),
    (lambda x: sum(x[0]) > 4, modifier.filter),
    (dewindowify, modifier.window),
    (lambda x, y: x + y, modifier.reduce)
]

apply_pipeline(iter(range(0, 10)), pipeline)
```
