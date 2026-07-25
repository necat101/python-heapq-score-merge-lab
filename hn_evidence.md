# HN Evidence

Hacker News thread: **Beating TimSort at Merging** — https://news.ycombinator.com/item?id=27823180
Linked article: https://earthly.dev/blog/python-timsort-merge/

## Linked article claims

- `heapq.merge` takes advantage of the fact that lists are already sorted, so we get a new sorted list in linear time rather than n*log(n) time for combining and sorting two unsorted lists.
- Python's `list.sort` is the original implementation of TimSort.
- TimSort is designed to find runs of sequential numbers and merge them together.

## Named Hacker News commenter claims

- **CogitoCogito** (https://news.ycombinator.com/item?id=27823851): "`heapq.merge()` is written in Python".
- **danbruc** (https://news.ycombinator.com/item?id=27824912): "The first Python implementation is bad – removing the first element in each iteration is O(n), the C implementation gets this right by maintaining one index into each list instead of modifying the lists."
- **jhokanson** (https://news.ycombinator.com/item?id=27823920): "Python doesn't provide a mergesort option [in list.sort], other than via heapq".

## Current Python documentation

From https://docs.python.org/3/library/heapq.html#heapq.merge:

- `heapq.merge(*iterables, key=None, reverse=False)` — Merge multiple sorted inputs into a single sorted output.
- `heapq.merge` is similar to `sorted(itertools.chain(*iterables))` but returns an iterable, does not pull the data into memory all at once, and assumes that each of the input streams is already sorted (smallest to largest).
- `key` function specifies a function of one argument that is used to extract a comparison key from each input element, default `None` (compare the elements directly).
- `reverse=True` is similar to having the key function return the elements in reverse order for all the inputs which are assumed to be sorted in reverse order.

## Local observations

- **sorted_score_stream_merge_marker**: `heapq.merge([0.10, 0.40, 0.70], [0.20, 0.50, 0.80])` produces `[0.10, 0.20, 0.40, 0.50, 0.70, 0.80]`, globally nondecreasing, all inputs preserved.
- **keyed_record_merge_marker**: `heapq.merge` with `key=lambda r: r["score"], reverse=True` correctly merges two descending record streams; ID order `["a1", "b1", "a2", "b2", "a3", "b3"]`, scores globally nonincreasing.
- **unsorted_input_precondition_marker**: `heapq.merge([0.10, 0.70, 0.40], [0.20, 0.50, 0.80])` raises no exception but produces `[0.10, 0.20, 0.5, 0.7, 0.4, 0.8]` – not globally sorted, differs from sorted concatenation.
- **lazy_merge_consumption_marker**: constructing `heapq.merge(gen_a, gen_b)` consumes zero source items; consuming 2 merged values yields `[0.10, 0.20]` with partial source consumption (< 6 total, >= 1 total); remainder yields `[0.40, 0.50, 0.70, 0.80]`; full output correct.

## HN thread retrieval

The HN thread was read with:

```
hackernews get-item --id 27823180
```

## Non-claims and limitations

This lab does **not** claim that:

- `heapq.merge` sorts unsorted inputs
- `heapq.merge` validates input ordering
- laziness means zero lookahead after iteration starts
- the lab proves bounded-memory behavior for every workload
- key-based merging resolves equal-score ties in a universally meaningful way
- the lab measures speed or proves performance superiority
- descending score order is always appropriate for ML pipelines

This lab does **not** cover:

- duplicate-score tie behavior
- empty streams
- three-way merges beyond the two-input cases used here
- top-k truncation
- mutable source streams
- concurrency
- external datasets
- performance measurements
- production ranking quality
