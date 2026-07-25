# Results

12/12 rows passed.

| Case | Method | Status | Message |
|------|--------|--------|---------|
| sorted_score_stream_merge_marker | inspect_inputs | PASS | inputs are two ascending sorted numeric streams with expected fixed values |
| sorted_score_stream_merge_marker | execute_merge | PASS | merge completed, output matches expected |
| sorted_score_stream_merge_marker | verify_relation | PASS | merged output is globally nondecreasing and contains every input value exactly once, matching expected order |
| keyed_record_merge_marker | inspect_inputs | PASS | inputs are two descending sorted record streams with distinct scores and expected fixed values |
| keyed_record_merge_marker | execute_merge | PASS | keyed merge completed with expected record count |
| keyed_record_merge_marker | verify_relation | PASS | merged ID order matches expected, scores globally nonincreasing, every input record preserved exactly once |
| unsorted_input_precondition_marker | inspect_inputs | PASS | stream_a contains exactly one deliberate inversion (0.70 before 0.40), stream_b is sorted |
| unsorted_input_precondition_marker | execute_merge | PASS | raw heapq.merge completed without exception (precondition violation not detected at runtime) |
| unsorted_input_precondition_marker | verify_relation | PASS | precondition violation confirmed: no exception raised, merged output is not globally sorted, differs from sorted concatenation |
| lazy_merge_consumption_marker | inspect_inputs | PASS | counting generators initialized with expected fixed values, zero initial yield counters |
| lazy_merge_consumption_marker | execute_merge | PASS | lazy merge executed: zero consumption at construction, correct prefix, correct full output |
| lazy_merge_consumption_marker | verify_relation | PASS | lazy consumption verified: zero at construction, correct prefix [0.10, 0.20], partial source consumption, correct suffix, full output correct, all source values yielded exactly once |

