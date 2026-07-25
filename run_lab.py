#!/usr/bin/env python3
"""
python-heapq-score-merge-lab

Four deterministic heapq.merge correctness markers:
  1. sorted_score_stream_merge_marker
  2. keyed_record_merge_marker
  3. unsorted_input_precondition_marker
  4. lazy_merge_consumption_marker

Each case runs: inspect_inputs → execute_merge → verify_relation
Total: 12 rows.
"""
import heapq
import json
from typing import Any

# ============================================================================
# Helpers
# ============================================================================

def is_nondecreasing(xs):
    return all(xs[i] <= xs[i+1] for i in range(len(xs)-1))

def is_nonincreasing(xs):
    return all(xs[i] >= xs[i+1] for i in range(len(xs)-1))

def multiset_equal(a, b):
    return sorted(a) == sorted(b)

# ============================================================================
# Case 1: sorted_score_stream_merge_marker
# ============================================================================

# Fixed inputs for case 1
C1_STREAM_A = [0.10, 0.40, 0.70]
C1_STREAM_B = [0.20, 0.50, 0.80]
C1_EXPECTED = [0.10, 0.20, 0.40, 0.50, 0.70, 0.80]

def c1_check_inputs(stream_a, stream_b):
    """Production input inspector for case 1 — callable with arbitrary inputs."""
    # required type/shape
    if not (isinstance(stream_a, list) and isinstance(stream_b, list)):
        return False, "inputs must be lists", {}
    # expected fixed values
    if stream_a != C1_STREAM_A:
        return False, f"stream_a has unexpected value: {stream_a}", {}
    if stream_b != C1_STREAM_B:
        return False, f"stream_b has unexpected value: {stream_b}", {}
    # ascending ordering
    if not is_nondecreasing(stream_a):
        return False, "stream_a not ascending", {}
    if not is_nondecreasing(stream_b):
        return False, "stream_b not ascending", {}
    details = {
        "stream_a": stream_a,
        "stream_b": stream_b,
        "a_sorted": True,
        "b_sorted": True,
    }
    return True, "inputs are two ascending sorted numeric streams with expected fixed values", details

def c1_inspect_inputs():
    """inspect_inputs for sorted_score_stream_merge_marker"""
    return c1_check_inputs(C1_STREAM_A, C1_STREAM_B)

def c1_execute_merge():
    """execute_merge for sorted_score_stream_merge_marker"""
    stream_a = C1_STREAM_A
    stream_b = C1_STREAM_B
    try:
        merged_iter = heapq.merge(stream_a, stream_b)
        merged = list(merged_iter)
    except Exception as e:
        return False, f"unexpected exception: {type(e).__name__}: {e}", {}
    expected = C1_EXPECTED
    details = {
        "inputs": {"stream_a": stream_a, "stream_b": stream_b},
        "merged": merged,
        "output_count": len(merged),
        "expected": expected,
    }
    ok = merged == expected
    msg = "merge completed, output matches expected" if ok else f"merge output {merged} != expected {expected}"
    return ok, msg, details

def c1_verify_relation():
    """verify_relation for sorted_score_stream_merge_marker"""
    stream_a = C1_STREAM_A
    stream_b = C1_STREAM_B
    merged = list(heapq.merge(stream_a, stream_b))
    expected = C1_EXPECTED

    if merged != expected:
        return False, f"merged output {merged} != expected {expected}", {}
    if not is_nondecreasing(merged):
        return False, "merged output not globally nondecreasing", {}
    all_inputs = stream_a + stream_b
    if not multiset_equal(merged, all_inputs):
        return False, "merged output does not contain every input value exactly once", {}

    details = {
        "merged": merged,
        "globally_nondecreasing": True,
        "multiset_preserved": True,
    }
    return True, "merged output is globally nondecreasing and contains every input value exactly once, matching expected order", details

# ============================================================================
# Case 2: keyed_record_merge_marker
# ============================================================================

C2_STREAM_A = [
    {"id": "a1", "score": 0.95},
    {"id": "a2", "score": 0.70},
    {"id": "a3", "score": 0.40},
]
C2_STREAM_B = [
    {"id": "b1", "score": 0.90},
    {"id": "b2", "score": 0.60},
    {"id": "b3", "score": 0.20},
]
C2_EXPECTED_IDS = ["a1", "b1", "a2", "b2", "a3", "b3"]

def c2_check_inputs(stream_a, stream_b):
    """Production input inspector for case 2 — callable with arbitrary inputs."""
    # type/shape
    if not (isinstance(stream_a, list) and isinstance(stream_b, list)):
        return False, "inputs must be lists", {}
    # required fields
    for rec in stream_a + stream_b:
        if not isinstance(rec, dict):
            return False, f"record not a dict: {rec}", {}
        if "id" not in rec or "score" not in rec:
            return False, f"record missing id/score: {rec}", {}
    # expected fixed values
    if stream_a != C2_STREAM_A:
        return False, f"stream_a unexpected: {stream_a}", {}
    if stream_b != C2_STREAM_B:
        return False, f"stream_b unexpected: {stream_b}", {}
    # descending ordering by score
    scores_a = [r["score"] for r in stream_a]
    scores_b = [r["score"] for r in stream_b]
    if not is_nonincreasing(scores_a):
        return False, "stream_a not descending", {}
    if not is_nonincreasing(scores_b):
        return False, "stream_b not descending", {}
    # distinct scores across all inputs
    all_scores = scores_a + scores_b
    if len(all_scores) != len(set(all_scores)):
        return False, f"scores not distinct: {all_scores}", {}
    details = {
        "stream_a": stream_a,
        "stream_b": stream_b,
        "a_descending": True,
        "b_descending": True,
        "all_scores_distinct": True,
    }
    return True, "inputs are two descending sorted record streams with distinct scores and expected fixed values", details

def c2_inspect_inputs():
    """inspect_inputs for keyed_record_merge_marker"""
    return c2_check_inputs(C2_STREAM_A, C2_STREAM_B)

def c2_execute_merge():
    """execute_merge for keyed_record_merge_marker"""
    stream_a = C2_STREAM_A
    stream_b = C2_STREAM_B
    key_fn = lambda record: record["score"]
    reverse = True
    try:
        merged_iter = heapq.merge(stream_a, stream_b, key=key_fn, reverse=reverse)
        merged = list(merged_iter)
    except Exception as e:
        return False, f"unexpected exception: {type(e).__name__}: {e}", {}

    merged_ids = [r["id"] for r in merged]
    details = {
        "inputs": {"stream_a": stream_a, "stream_b": stream_b},
        "merge_args": {"key": "lambda record: record[\"score\"]", "reverse": True},
        "merged": merged,
        "merged_ids": merged_ids,
        "output_count": len(merged),
    }
    ok = len(merged) == 6
    msg = "keyed merge completed with expected record count" if ok else f"unexpected output count: {len(merged)}"
    return ok, msg, details

def c2_verify_relation():
    """verify_relation for keyed_record_merge_marker"""
    stream_a = C2_STREAM_A
    stream_b = C2_STREAM_B
    merged = list(heapq.merge(stream_a, stream_b, key=lambda r: r["score"], reverse=True))
    merged_ids = [r["id"] for r in merged]
    expected_ids = C2_EXPECTED_IDS

    if merged_ids != expected_ids:
        return False, f"merged ID order {merged_ids} != expected {expected_ids}", {}

    merged_scores = [r["score"] for r in merged]
    if not is_nonincreasing(merged_scores):
        return False, f"merged scores not globally nonincreasing: {merged_scores}", {}

    # preservation: every input record appears exactly once
    input_ids = [r["id"] for r in stream_a + stream_b]
    if sorted(merged_ids) != sorted(input_ids):
        return False, "not all input records preserved", {}
    if len(merged_ids) != len(set(merged_ids)):
        return False, "duplicate records in merged output", {}

    # also check full record equality
    input_map = {r["id"]: r for r in stream_a + stream_b}
    for r in merged:
        if r["id"] not in input_map or input_map[r["id"]] != r:
            return False, f"record mismatch for id {r['id']}", {}

    details = {
        "merged_ids": merged_ids,
        "merged_scores": merged_scores,
        "scores_globally_nonincreasing": True,
        "all_records_preserved": True,
    }
    return True, "merged ID order matches expected, scores globally nonincreasing, every input record preserved exactly once", details

# ============================================================================
# Case 3: unsorted_input_precondition_marker
# ============================================================================

C3_STREAM_A = [0.10, 0.70, 0.40]
C3_STREAM_B = [0.20, 0.50, 0.80]

def c3_check_inputs(stream_a, stream_b):
    """Production input inspector for case 3 — callable with arbitrary inputs."""
    # type/shape
    if not (isinstance(stream_a, list) and isinstance(stream_b, list)):
        return False, "inputs must be lists", {}
    # expected fixed values
    if stream_a != C3_STREAM_A:
        return False, f"stream_a unexpected: {stream_a}", {}
    if stream_b != C3_STREAM_B:
        return False, f"stream_b unexpected: {stream_b}", {}
    # stream_b must be ascending
    if not is_nondecreasing(stream_b):
        return False, "stream_b not ascending (should be sorted)", {}
    # stream_a must violate ascending order in exactly one place
    inversions = [(i, stream_a[i], stream_a[i+1]) for i in range(len(stream_a)-1) if stream_a[i] > stream_a[i+1]]
    if len(inversions) != 1:
        return False, f"stream_a must have exactly one inversion, found {len(inversions)}: {inversions}", {}
    inv_i, inv_x, inv_y = inversions[0]
    if not (inv_i == 1 and inv_x == 0.70 and inv_y == 0.40):
        return False, f"unexpected inversion: index {inv_i}: {inv_x} > {inv_y}", {}
    details = {
        "stream_a": stream_a,
        "stream_b": stream_b,
        "stream_a_sorted": False,
        "stream_b_sorted": True,
        "inversions": inversions,
    }
    return True, "stream_a contains exactly one deliberate inversion (0.70 before 0.40), stream_b is sorted", details

def c3_inspect_inputs():
    """inspect_inputs for unsorted_input_precondition_marker"""
    return c3_check_inputs(C3_STREAM_A, C3_STREAM_B)

def c3_execute_merge():
    """execute_merge for unsorted_input_precondition_marker"""
    stream_a = C3_STREAM_A
    stream_b = C3_STREAM_B

    exception_type = None
    exception_msg = None
    try:
        merged_iter = heapq.merge(stream_a, stream_b)
        merged = list(merged_iter)
    except Exception as e:
        exception_type = type(e).__name__
        exception_msg = str(e)
        merged = None

    details = {
        "inputs": {"stream_a": stream_a, "stream_b": stream_b},
        "merged": merged,
        "output_count": len(merged) if merged is not None else 0,
        "exception_type": exception_type,
        "exception_msg": exception_msg,
    }
    # execution succeeds if no exception was raised and we got output
    ok = exception_type is None and merged is not None
    msg = "raw heapq.merge completed without exception (precondition violation not detected at runtime)" if ok else f"unexpected exception: {exception_type}: {exception_msg}"
    return ok, msg, details

def c3_verify_relation():
    """verify_relation for unsorted_input_precondition_marker"""
    stream_a = C3_STREAM_A
    stream_b = C3_STREAM_B

    # confirm precondition violation
    if is_nondecreasing(stream_a):
        return False, "stream_a is sorted, precondition violation not present", {}

    exception_type = None
    try:
        merged = list(heapq.merge(stream_a, stream_b))
    except Exception as e:
        exception_type = type(e).__name__
        merged = None

    if exception_type is not None:
        return False, f"heapq.merge raised {exception_type}, expected no exception", {}

    # merged output must NOT be globally sorted
    if is_nondecreasing(merged):
        return False, f"merged output is unexpectedly globally sorted: {merged}", {}

    # merged output must differ from correctly sorted concatenation
    correctly_sorted = sorted(stream_a + stream_b)
    if merged == correctly_sorted:
        return False, f"merged output unexpectedly equals correctly sorted concatenation: {merged}", {}

    details = {
        "merged": merged,
        "correctly_sorted": correctly_sorted,
        "merged_is_sorted": False,
        "merged_equals_sorted_concat": False,
        "exception_raised": False,
    }
    return True, "precondition violation confirmed: no exception raised, merged output is not globally sorted, differs from sorted concatenation", details

# ============================================================================
# Case 4: lazy_merge_consumption_marker
# ============================================================================

class CountingGen:
    def __init__(self, values, name):
        self.values = list(values)
        self.name = name
        self.yield_count = 0
        self.yielded_values = []

    def __iter__(self):
        for v in self.values:
            self.yield_count += 1
            self.yielded_values.append(v)
            yield v

C4_STREAM_A_VALUES = [0.10, 0.40, 0.70]
C4_STREAM_B_VALUES = [0.20, 0.50, 0.80]

def c4_check_inputs(gen_a, gen_b):
    """Production input inspector for case 4 — callable with arbitrary generators."""
    # zero initial lazy-generator counters
    if gen_a.yield_count != 0:
        return False, f"gen_a initial yield_count != 0: {gen_a.yield_count}", {}
    if gen_b.yield_count != 0:
        return False, f"gen_b initial yield_count != 0: {gen_b.yield_count}", {}
    # expected fixed values
    if gen_a.values != C4_STREAM_A_VALUES:
        return False, f"gen_a values unexpected: {gen_a.values}", {}
    if gen_b.values != C4_STREAM_B_VALUES:
        return False, f"gen_b values unexpected: {gen_b.values}", {}
    details = {
        "stream_a_values": C4_STREAM_A_VALUES,
        "stream_b_values": C4_STREAM_B_VALUES,
        "initial_yield_count_a": gen_a.yield_count,
        "initial_yield_count_b": gen_b.yield_count,
    }
    return True, "counting generators initialized with expected fixed values, zero initial yield counters", details

def c4_inspect_inputs():
    """inspect_inputs for lazy_merge_consumption_marker"""
    gen_a = CountingGen(C4_STREAM_A_VALUES, "a")
    gen_b = CountingGen(C4_STREAM_B_VALUES, "b")
    return c4_check_inputs(gen_a, gen_b)

def c4_execute_merge():
    """execute_merge for lazy_merge_consumption_marker"""
    stream_a_values = C4_STREAM_A_VALUES
    stream_b_values = C4_STREAM_B_VALUES

    gen_a = CountingGen(stream_a_values, "a")
    gen_b = CountingGen(stream_b_values, "b")

    prefix_len = 2
    expected_prefix = [0.10, 0.20]
    expected_suffix = [0.40, 0.50, 0.70, 0.80]
    expected_full = [0.10, 0.20, 0.40, 0.50, 0.70, 0.80]

    try:
        merged_iter = heapq.merge(gen_a, gen_b)
        count_a_at_construction = gen_a.yield_count
        count_b_at_construction = gen_b.yield_count

        # consume prefix
        prefix = []
        it = iter(merged_iter)
        for _ in range(prefix_len):
            try:
                prefix.append(next(it))
            except StopIteration:
                break
        count_a_after_prefix = gen_a.yield_count
        count_b_after_prefix = gen_b.yield_count

        # consume remainder
        suffix = list(it)
        count_a_final = gen_a.yield_count
        count_b_final = gen_b.yield_count

    except Exception as e:
        return False, f"unexpected exception: {type(e).__name__}: {e}", {}

    full_output = prefix + suffix
    details = {
        "inputs": {"stream_a": stream_a_values, "stream_b": stream_b_values},
        "prefix_len": prefix_len,
        "prefix": prefix,
        "suffix": suffix,
        "full_output": full_output,
        "counts": {
            "at_construction": {"a": count_a_at_construction, "b": count_b_at_construction},
            "after_prefix": {"a": count_a_after_prefix, "b": count_b_after_prefix},
            "final": {"a": count_a_final, "b": count_b_final},
        },
        "expected_prefix": expected_prefix,
        "expected_suffix": expected_suffix,
        "expected_full": expected_full,
    }

    # execution row: confirm merge interaction completed with expected broad structure
    if count_a_at_construction != 0 or count_b_at_construction != 0:
        return False, f"counters nonzero at construction: a={count_a_at_construction}, b={count_b_at_construction}", details
    if prefix != expected_prefix:
        return False, f"prefix {prefix} != expected {expected_prefix}", details
    if full_output != expected_full:
        return False, f"full_output {full_output} != expected {expected_full}", details

    return True, "lazy merge executed: zero consumption at construction, correct prefix, correct full output", details

def c4_verify_relation():
    """verify_relation for lazy_merge_consumption_marker"""
    stream_a_values = C4_STREAM_A_VALUES
    stream_b_values = C4_STREAM_B_VALUES

    gen_a = CountingGen(stream_a_values, "a")
    gen_b = CountingGen(stream_b_values, "b")

    merged_iter = heapq.merge(gen_a, gen_b)

    # constructing heapq.merge(...) leaves both yield counters at zero
    if gen_a.yield_count != 0 or gen_b.yield_count != 0:
        return False, f"counters nonzero at construction: a={gen_a.yield_count}, b={gen_b.yield_count}", {}

    # consuming two merged values yields [0.10, 0.20]
    it = iter(merged_iter)
    prefix = [next(it), next(it)]
    expected_prefix = [0.10, 0.20]
    if prefix != expected_prefix:
        return False, f"prefix {prefix} != expected {expected_prefix}", {}

    count_a_after_prefix = gen_a.yield_count
    count_b_after_prefix = gen_b.yield_count

    # at least one source item consumed after iteration begins
    total_consumed_after_prefix = count_a_after_prefix + count_b_after_prefix
    if total_consumed_after_prefix < 1:
        return False, f"no source items consumed after prefix: a={count_a_after_prefix}, b={count_b_after_prefix}", {}

    # fewer than all six source items consumed after that prefix
    if total_consumed_after_prefix >= 6:
        return False, f"all source items consumed after prefix (not lazy): a={count_a_after_prefix}, b={count_b_after_prefix}", {}

    # consuming the remainder yields [0.40, 0.50, 0.70, 0.80]
    suffix = list(it)
    expected_suffix = [0.40, 0.50, 0.70, 0.80]
    if suffix != expected_suffix:
        return False, f"suffix {suffix} != expected {expected_suffix}", {}

    full_output = prefix + suffix
    expected_full = [0.10, 0.20, 0.40, 0.50, 0.70, 0.80]
    if full_output != expected_full:
        return False, f"full_output {full_output} != expected {expected_full}", {}

    # each source generator eventually yields each of its three values exactly once
    if gen_a.yield_count != 3:
        return False, f"gen_a yield_count = {gen_a.yield_count}, expected 3", {}
    if gen_b.yield_count != 3:
        return False, f"gen_b yield_count = {gen_b.yield_count}, expected 3", {}
    if gen_a.yielded_values != stream_a_values:
        return False, f"gen_a yielded {gen_a.yielded_values} != {stream_a_values}", {}
    if gen_b.yielded_values != stream_b_values:
        return False, f"gen_b yielded {gen_b.yielded_values} != {stream_b_values}", {}

    details = {
        "prefix": prefix,
        "suffix": suffix,
        "full_output": full_output,
        "counts_after_prefix": {"a": count_a_after_prefix, "b": count_b_after_prefix},
        "final_counts": {"a": gen_a.yield_count, "b": gen_b.yield_count},
        "all_values_yielded_exactly_once": True,
    }
    return True, "lazy consumption verified: zero at construction, correct prefix [0.10, 0.20], partial source consumption, correct suffix, full output correct, all source values yielded exactly once", details

# ============================================================================
# Dispatcher
# ============================================================================

CASES = {
    "sorted_score_stream_merge_marker": {
        "inspect_inputs": c1_inspect_inputs,
        "execute_merge": c1_execute_merge,
        "verify_relation": c1_verify_relation,
    },
    "keyed_record_merge_marker": {
        "inspect_inputs": c2_inspect_inputs,
        "execute_merge": c2_execute_merge,
        "verify_relation": c2_verify_relation,
    },
    "unsorted_input_precondition_marker": {
        "inspect_inputs": c3_inspect_inputs,
        "execute_merge": c3_execute_merge,
        "verify_relation": c3_verify_relation,
    },
    "lazy_merge_consumption_marker": {
        "inspect_inputs": c4_inspect_inputs,
        "execute_merge": c4_execute_merge,
        "verify_relation": c4_verify_relation,
    },
}

METHOD_ORDER = ["inspect_inputs", "execute_merge", "verify_relation"]

def run_case_method(case_name, method_name):
    fn = CASES[case_name][method_name]
    try:
        ok, message, details = fn()
    except Exception as e:
        ok = False
        message = f"unhandled exception in {case_name}.{method_name}: {type(e).__name__}: {e}"
        details = {}
    return {
        "case": case_name,
        "method": method_name,
        "ok": bool(ok),
        "message": message,
        "details": details,
    }

def main():
    rows = []
    for case_name in CASES:
        for method_name in METHOD_ORDER:
            row = run_case_method(case_name, method_name)
            rows.append(row)
            status = "PASS" if row["ok"] else "FAIL"
            print(f"[{status}] {case_name} :: {method_name} — {row['message']}")

    # write observations.json
    with open("observations.json", "w") as f:
        json.dump(rows, f, indent=2)

    # write RESULTS.md
    passed = sum(1 for r in rows if r["ok"])
    total = len(rows)
    with open("RESULTS.md", "w") as f:
        f.write("# Results\n\n")
        f.write(f"{passed}/{total} rows passed.\n\n")
        f.write("| Case | Method | Status | Message |\n")
        f.write("|------|--------|--------|---------|\n")
        for r in rows:
            status = "PASS" if r["ok"] else "FAIL"
            msg = r["message"].replace("|", "\\|").replace("\n", " ")
            f.write(f"| {r['case']} | {r['method']} | {status} | {msg} |\n")
        f.write("\n")

    print(f"\n{passed}/{total} rows passed.")
    print("Wrote observations.json and RESULTS.md")
    return 0 if passed == total else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
