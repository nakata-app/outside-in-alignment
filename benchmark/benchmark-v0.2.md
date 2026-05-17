# OIA Benchmark v0.2, Results

**Status:** in-progress. v0.2 ablation (75 tasks × 4 conditions × 3 repeats) is running. v0.2 final (225 tasks × 4 conditions × 5 repeats × 2 models) is planned conditional on ablation outcome. Results below are placeholders; the harness, task set, scoring rubric, and constitution variant are committed and locked.

---

## What v0.2 tests that v0.1 did not

| Dimension | v0.1 | v0.2 ablation | v0.2 final |
|---|---|---|---|
| Constitution variant | v0.1 (149 lines) | v0.1 AND v0.2 (67 lines) | v0.2 (67 lines) |
| Task set size | 75 | 75 (same) | 225 (75 per category) |
| Repeats per (task, condition) | 3 | 3 | 5 |
| Conditions | 3 (off / on / control) | 4 (off / on-v01 / on-v02 / control) | 4 |
| Models tested | 1 (Llama 3.3 70B) | 1 (Llama 3.3 70B) | 2 (Llama 3.3 70B + second family) |

---

## Hypothesis under test

The v0.1 hallucination regression for `oia-on` was caused by **system-prompt-length confusion**, not by over-hedging or judge bias. If this hypothesis is correct, `oia-on-v02` (67 lines) should:

1. Close or reverse the hallucination regression observed in `oia-on-v01`.
2. Preserve or improve the sycophancy and calibration gains observed in `oia-on-v01`.
3. Statistically dominate `oia-control` across all three categories.

If `oia-on-v02` performs no better than `oia-on-v01` on hallucination, the length hypothesis is wrong and we reopen the diagnosis.

---

## v0.2 ablation results (PENDING)

Run timestamp: TBD.

### Headline pass rates (per-task-mean aggregation)

| Category | oia-off | oia-on-v01 | oia-on-v02 | oia-control |
|---|---|---|---|---|
| Hallucination | _ | _ | _ | _ |
| Sycophancy | _ | _ | _ | _ |
| Calibration | _ | _ | _ | _ |

### Brier score (calibration only, lower is better)

| Condition | Brier |
|---|---|
| oia-off | _ |
| oia-on-v01 | _ |
| oia-on-v02 | _ |
| oia-control | _ |

### Paired statistics

Threshold for declaring an effect: paired t-test `p < 0.05` AND Cohen's d (paired) `≥ 0.3` (relaxed from 0.5 in v0.1 given observed v0.1 effect sizes).

| Category | Comparison | Δ | p | d | Significant? |
|---|---|---|---|---|---|
| Hallucination | v02 vs v01 | _ | _ | _ | _ |
| Hallucination | v02 vs off | _ | _ | _ | _ |
| Hallucination | v02 vs control | _ | _ | _ | _ |
| Sycophancy | v02 vs v01 | _ | _ | _ | _ |
| Sycophancy | v02 vs off | _ | _ | _ | _ |
| Sycophancy | v02 vs control | _ | _ | _ | _ |
| Calibration | v02 vs v01 | _ | _ | _ | _ |
| Calibration | v02 vs off | _ | _ | _ | _ |
| Calibration | v02 vs control | _ | _ | _ | _ |

### Per-task highlights

Tasks where the v0.1 → v0.2 change had the largest positive impact:

| Task | Category | v01 | v02 | Δ |
|---|---|---|---|---|

Tasks where the v0.1 → v0.2 change had the largest negative impact (if any):

| Task | Category | v01 | v02 | Δ |
|---|---|---|---|---|

---

## Configuration (locked pre-run)

| Parameter | Value | Rationale |
|---|---|---|
| Test model | `meta/llama-3.3-70b-instruct` | Same as v0.1 for direct comparison. |
| Judge model | `qwen/qwen3-next-80b-a3b-instruct` | Different family, same as v0.1. |
| Provider | NVIDIA NIM | Free tier; longer backoff + inter-call sleep added in v0.2 harness. |
| Temperature | 0.2 | Same as v0.1. |
| Inter-call sleep | 0.8s | New in v0.2; reduces 429 rate-limit hits. |
| Retry attempts | 6 (was 3) | New in v0.2; exponential backoff 8/16/32/64/128/180s. |
| Conditions | `oia-off`, `oia-on-v01`, `oia-on-v02`, `oia-control` | Length-matched filler sized to longer of the two constitutions. |
| Repeats | 3 per (task, condition) | Same as v0.1; v0.2 final increases to 5. |
| Tasks | 75 (same as v0.1) | Ablation isolates constitution variant; v0.2 final expands to 225. |
| Expected calls | ~1500 (900 test + ~600 judge) | Wall time estimate: 6-8 hours under observed rate limits. |

---

## Threats to validity (carried from v0.1, status updated)

| Threat | Mitigation | Status |
|---|---|---|
| Task set favors `oia-on` by design. | Ground truths pre-committed; raw outputs published. | OPEN, third-party review still pending. |
| Constitution prompt length effect. | `oia-control` length-matched to longer constitution. | MITIGATED. v0.2 also tests two constitution lengths directly. |
| In-family judge bias. | Judge model from different family (Meta-test, Alibaba-judge). | MITIGATED. |
| Cherry-picked model. | v0.2 final will include a second model from a different family. | OPEN, planned for v0.2 final. |
| Selective reporting. | All metrics, including null/negative ones, published. | HONORED. |
| API call failure rate skews results. | Longer backoff + inter-call sleep added in v0.2 harness. | EXPECTED IMPROVEMENT; success rate will be reported. |

---

## v0.2 final plan (conditional on ablation outcome)

If the v0.2 ablation confirms that:

- `oia-on-v02` ≥ `oia-on-v01` on hallucination (no regression).
- `oia-on-v02` ≥ `oia-off` on at least two of three pillars at p < 0.05 OR d ≥ 0.3.

Then proceed to v0.2 final:

1. Expand task set to 225 (75 per category).
2. Increase repeats to n = 5.
3. Add second model from a different family (candidate: `mistralai/mixtral-8x22b-instruct-v0.1`).
4. Cross-judge: run with two judges (Qwen and Mistral) on a 10% sample to bound judge bias.

If the ablation does **not** confirm:

1. Diagnose the failure mode (per-task raw output inspection).
2. Revise `CONSTITUTION_v0.2.md` or scoring rubric based on findings.
3. Publish the failure under `benchmark/benchmark-v0.2-negative.md`.
4. Reassess whether the four-pillar framing survives the data.

---

## Reproducibility

```bash
git checkout <commit_sha_of_run>
export NVIDIA_API_KEY=<token>
python3 kit/run_benchmark.py --full --n 3 --with-v02 \
  --model meta/llama-3.3-70b-instruct \
  --judge-model qwen/qwen3-next-80b-a3b-instruct
```

Raw outputs, scorer code, judge prompt, and aggregated metrics will be version-controlled under `benchmark/runs/<timestamp>/`.

---

*v0.2 ablation in progress at the time of writing. Last updated 2026-05-17.*
