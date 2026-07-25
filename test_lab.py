#!/usr/bin/env python3
"""Independent tests for python-heapq-score-merge-lab."""
import unittest
import heapq
import run_lab


def is_nondecreasing(xs):
    return all(xs[i] <= xs[i+1] for i in range(len(xs)-1))

def is_nonincreasing(xs):
    return all(xs[i] >= xs[i+1] for i in range(len(xs)-1))


class TestSortedScoreStreamMerge(unittest.TestCase):
    def test_exact_ascending_numeric_merged_output(self):
        stream_a = [0.10, 0.40, 0.70]
        stream_b = [0.20, 0.50, 0.80]
        merged = list(heapq.merge(stream_a, stream_b))
        self.assertEqual(merged, [0.10, 0.20, 0.40, 0.50, 0.70, 0.80])

    def test_global_nondecreasing_ordering(self):
        stream_a = [0.10, 0.40, 0.70]
        stream_b = [0.20, 0.50, 0.80]
        merged = list(heapq.merge(stream_a, stream_b))
        self.assertTrue(is_nondecreasing(merged))

    def test_preservation_of_every_numeric_input_occurrence(self):
        stream_a = [0.10, 0.40, 0.70]
        stream_b = [0.20, 0.50, 0.80]
        merged = list(heapq.merge(stream_a, stream_b))
        all_inputs = stream_a + stream_b
        self.assertEqual(sorted(merged), sorted(all_inputs))
        self.assertEqual(len(merged), len(all_inputs))


class TestKeyedRecordMerge(unittest.TestCase):
    def test_exact_keyed_record_id_order(self):
        stream_a = [
            {"id": "a1", "score": 0.95},
            {"id": "a2", "score": 0.70},
            {"id": "a3", "score": 0.40},
        ]
        stream_b = [
            {"id": "b1", "score": 0.90},
            {"id": "b2", "score": 0.60},
            {"id": "b3", "score": 0.20},
        ]
        merged = list(heapq.merge(stream_a, stream_b, key=lambda r: r["score"], reverse=True))
        merged_ids = [r["id"] for r in merged]
        self.assertEqual(merged_ids, ["a1", "b1", "a2", "b2", "a3", "b3"])

    def test_global_nonincreasing_keyed_scores(self):
        stream_a = [
            {"id": "a1", "score": 0.95},
            {"id": "a2", "score": 0.70},
            {"id": "a3", "score": 0.40},
        ]
        stream_b = [
            {"id": "b1", "score": 0.90},
            {"id": "b2", "score": 0.60},
            {"id": "b3", "score": 0.20},
        ]
        merged = list(heapq.merge(stream_a, stream_b, key=lambda r: r["score"], reverse=True))
        merged_scores = [r["score"] for r in merged]
        self.assertTrue(is_nonincreasing(merged_scores))

    def test_preservation_of_every_keyed_input_record(self):
        stream_a = [
            {"id": "a1", "score": 0.95},
            {"id": "a2", "score": 0.70},
            {"id": "a3", "score": 0.40},
        ]
        stream_b = [
            {"id": "b1", "score": 0.90},
            {"id": "b2", "score": 0.60},
            {"id": "b3", "score": 0.20},
        ]
        merged = list(heapq.merge(stream_a, stream_b, key=lambda r: r["score"], reverse=True))
        input_ids = [r["id"] for r in stream_a + stream_b]
        merged_ids = [r["id"] for r in merged]
        self.assertEqual(sorted(merged_ids), sorted(input_ids))
        self.assertEqual(len(merged_ids), len(set(merged_ids)))
        input_map = {r["id"]: r for r in stream_a + stream_b}
        for r in merged:
            self.assertIn(r["id"], input_map)
            self.assertEqual(input_map[r["id"]], r)


class TestUnsortedInputPrecondition(unittest.TestCase):
    def test_unsorted_inspector_detects_deliberate_inversion(self):
        ok, msg, details = run_lab.c3_inspect_inputs()
        self.assertTrue(ok)
        self.assertFalse(details["stream_a_sorted"])
        self.assertEqual(details["inversions"], [(1, 0.70, 0.40)])

    def test_raw_merge_of_unsorted_input_raises_no_exception(self):
        stream_a = [0.10, 0.70, 0.40]
        stream_b = [0.20, 0.50, 0.80]
        exception_raised = False
        try:
            merged = list(heapq.merge(stream_a, stream_b))
        except Exception:
            exception_raised = True
        self.assertFalse(exception_raised)

    def test_unsorted_merged_result_is_not_globally_sorted(self):
        stream_a = [0.10, 0.70, 0.40]
        stream_b = [0.20, 0.50, 0.80]
        merged = list(heapq.merge(stream_a, stream_b))
        self.assertFalse(is_nondecreasing(merged))

    def test_unsorted_merged_result_differs_from_sorted_concatenation(self):
        stream_a = [0.10, 0.70, 0.40]
        stream_b = [0.20, 0.50, 0.80]
        merged = list(heapq.merge(stream_a, stream_b))
        correctly_sorted = sorted(stream_a + stream_b)
        self.assertNotEqual(merged, correctly_sorted)


class TestLazyMergeConsumption(unittest.TestCase):
    def test_constructing_lazy_merged_iterator_consumes_zero_source_items(self):
        gen_a = run_lab.CountingGen([0.10, 0.40, 0.70], "a")
        gen_b = run_lab.CountingGen([0.20, 0.50, 0.80], "b")
        merged_iter = heapq.merge(gen_a, gen_b)
        self.assertEqual(gen_a.yield_count, 0)
        self.assertEqual(gen_b.yield_count, 0)

    def test_two_item_prefix_equals_expected(self):
        gen_a = run_lab.CountingGen([0.10, 0.40, 0.70], "a")
        gen_b = run_lab.CountingGen([0.20, 0.50, 0.80], "b")
        merged_iter = heapq.merge(gen_a, gen_b)
        it = iter(merged_iter)
        prefix = [next(it), next(it)]
        self.assertEqual(prefix, [0.10, 0.20])

    def test_partial_consumption_does_not_exhaust_all_source_items(self):
        gen_a = run_lab.CountingGen([0.10, 0.40, 0.70], "a")
        gen_b = run_lab.CountingGen([0.20, 0.50, 0.80], "b")
        merged_iter = heapq.merge(gen_a, gen_b)
        it = iter(merged_iter)
        next(it); next(it)
        total_consumed = gen_a.yield_count + gen_b.yield_count
        self.assertGreaterEqual(total_consumed, 1)
        self.assertLess(total_consumed, 6)

    def test_final_suffix_and_complete_lazy_result_are_exact(self):
        gen_a = run_lab.CountingGen([0.10, 0.40, 0.70], "a")
        gen_b = run_lab.CountingGen([0.20, 0.50, 0.80], "b")
        merged_iter = heapq.merge(gen_a, gen_b)
        it = iter(merged_iter)
        prefix = [next(it), next(it)]
        suffix = list(it)
        self.assertEqual(prefix, [0.10, 0.20])
        self.assertEqual(suffix, [0.40, 0.50, 0.70, 0.80])
        self.assertEqual(prefix + suffix, [0.10, 0.20, 0.40, 0.50, 0.70, 0.80])


# ============================================================================
# Corruption tests — call actual production helpers via dispatcher path
# ============================================================================

class TestCorruptionRejection(unittest.TestCase):
    """All four production input inspectors reject deliberately corrupted inputs."""

    def test_c1_rejects_descending_replacement_for_ascending_stream(self):
        # c1 expects ascending streams; feed descending
        # calls actual production helper run_lab.c1_check_inputs
        ok, msg, _ = run_lab.c1_check_inputs([0.70, 0.40, 0.10], [0.20, 0.50, 0.80])
        self.assertFalse(ok)
        # fails on unexpected fixed value check (which runs before ordering check)
        self.assertIn("unexpected value", msg.lower())

    def test_c2_rejects_keyed_record_missing_score(self):
        stream_a = [
            {"id": "a1", "score": 0.95},
            {"id": "a2"},  # missing score
            {"id": "a3", "score": 0.40},
        ]
        stream_b = [
            {"id": "b1", "score": 0.90},
            {"id": "b2", "score": 0.60},
            {"id": "b3", "score": 0.20},
        ]
        # calls actual production helper run_lab.c2_check_inputs
        ok, msg, _ = run_lab.c2_check_inputs(stream_a, stream_b)
        self.assertFalse(ok)
        self.assertIn("missing id/score", msg.lower())

    def test_c3_rejects_allegedly_unsorted_case_with_no_inversion(self):
        # c3 expects exactly one inversion at index 1 (0.70 > 0.40)
        # feed a sorted stream instead
        # calls actual production helper run_lab.c3_check_inputs
        ok, msg, _ = run_lab.c3_check_inputs([0.10, 0.40, 0.70], [0.20, 0.50, 0.80])
        self.assertFalse(ok)
        # fails either on unexpected fixed value or inversion count
        self.assertTrue("unexpected" in msg.lower() or "inversion" in msg.lower())

    def test_c4_rejects_nonzero_initial_lazy_counters(self):
        gen_a = run_lab.CountingGen([0.10, 0.40, 0.70], "a")
        gen_b = run_lab.CountingGen([0.20, 0.50, 0.80], "b")
        # corrupt: consume one item before inspection
        next(iter(gen_a))
        # calls actual production helper run_lab.c4_check_inputs
        ok, msg, _ = run_lab.c4_check_inputs(gen_a, gen_b)
        self.assertFalse(ok)
        self.assertIn("yield_count != 0", msg)


class TestLabRows(unittest.TestCase):
    """The twelve rows are deterministic, unique, and in the required order."""

    def test_twelve_rows_deterministic_unique_ordered(self):
        rows1 = []
        for case_name in run_lab.CASES:
            for method_name in run_lab.METHOD_ORDER:
                rows1.append(run_lab.run_case_method(case_name, method_name))
        rows2 = []
        for case_name in run_lab.CASES:
            for method_name in run_lab.METHOD_ORDER:
                rows2.append(run_lab.run_case_method(case_name, method_name))

        self.assertEqual(len(rows1), 12)
        self.assertEqual(len(rows2), 12)

        # deterministic: same results twice
        for r1, r2 in zip(rows1, rows2):
            self.assertEqual(r1["case"], r2["case"])
            self.assertEqual(r1["method"], r2["method"])
            self.assertEqual(r1["ok"], r2["ok"])

        # unique
        seen = set()
        for r in rows1:
            key = (r["case"], r["method"])
            self.assertNotIn(key, seen, f"duplicate row: {key}")
            seen.add(key)

        # required order
        expected = [
            ("sorted_score_stream_merge_marker", "inspect_inputs"),
            ("sorted_score_stream_merge_marker", "execute_merge"),
            ("sorted_score_stream_merge_marker", "verify_relation"),
            ("keyed_record_merge_marker", "inspect_inputs"),
            ("keyed_record_merge_marker", "execute_merge"),
            ("keyed_record_merge_marker", "verify_relation"),
            ("unsorted_input_precondition_marker", "inspect_inputs"),
            ("unsorted_input_precondition_marker", "execute_merge"),
            ("unsorted_input_precondition_marker", "verify_relation"),
            ("lazy_merge_consumption_marker", "inspect_inputs"),
            ("lazy_merge_consumption_marker", "execute_merge"),
            ("lazy_merge_consumption_marker", "verify_relation"),
        ]
        actual = [(r["case"], r["method"]) for r in rows1]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
