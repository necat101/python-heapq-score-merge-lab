# python-heapq-score-merge-lab

A tiny deterministic stdlib-only correctness lab for merging already-sorted score streams with `heapq.merge`.

Hacker News thread: **Beating TimSort at Merging** — https://news.ycombinator.com/item?id=27823180

## What it does

Four fixed test cases, three methods each = twelve rows total.

1. **sorted_score_stream_merge_marker** — two ascending numeric streams `[0.10, 0.40, 0.70]` and `[0.20, 0.50, 0.80]` merge to `[0.10, 0.20, 0.40, 0.50, 0.70, 0.80]`
2. **keyed_record_merge_marker** — two descending record streams with `key=lambda r: r["score"], reverse=True`; verifies exact ID order `["a1", "b1", "a2", "b2", "a3", "b3"]`
3. **unsorted_input_precondition_marker** — one deliberately inverted input `[0.10, 0.70, 0.40]`; `heapq.merge` produces incorrectly ordered output with no exception raised
4. **lazy_merge_consumption_marker** — counting generators verify zero consumption at iterator construction, partial consumption after a short prefix, correct prefix/suffix, and full output correctness

Each case runs: `inspect_inputs` → `execute_merge` → `verify_relation`.

## Run

```bash
python3 run_lab.py
python3 -m unittest test_lab -v
```

No dependencies beyond the Python standard library. Python 3.11+ recommended.

## Files

- `run_lab.py` — production lab code, four cases × three methods
- `test_lab.py` — independent unittest suite
- `observations.json` — machine-readable results (generated)
- `RESULTS.md` — pass/fail matrix (generated)
- `hn_evidence.md` / `hn_evidence.jsonl` — HN thread claims, Python docs, local observations
- `hn_story_27823180.json` — raw HN API response for thread 27823180

## What this lab does NOT claim

- `heapq.merge` sorts unsorted inputs
- `heapq.merge` validates input ordering
- laziness means zero lookahead after iteration starts
- the lab proves bounded-memory behavior for every workload
- key-based merging resolves equal-score ties in a universally meaningful way
- the lab measures speed or proves performance superiority
- descending score order is always appropriate for ML pipelines

## Out of scope

- duplicate-score tie behavior
- empty streams
- three-way merges
- top-k truncation
- mutable source streams
- concurrency
- external datasets
- performance measurements
- production ranking quality
