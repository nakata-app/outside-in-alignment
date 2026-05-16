# OIA Benchmark v0.1, Results

**Status:** in-progress. Results below are placeholders until the full run completes. The harness, task set, and scoring rubric are committed and locked.

---

## Configuration

| Parameter | Value | Rationale |
|---|---|---|
| Test model | `meta/llama-3.3-70b-instruct` | Standard instruct, not reasoning. The OIA hypothesis is that the constitution disciplines a baseline model; reasoning models can mask the effect. |
| Judge model | `qwen/qwen2.5-72b-instruct` | Different model family (Alibaba vs Meta) reduces in-family judge bias. |
| Provider | NVIDIA NIM (`integrate.api.nvidia.com/v1`) | Free tier, OpenAI-compatible. |
| Temperature | 0.2 | Reduces noise without freezing the distribution. |
| Max tokens | 1024 | Sufficient for all task categories. |
| Conditions | `oia-off`, `oia-on`, `oia-control` | Three-way comparison rules out 'more context = better answer'. |
| Repeats per (task, condition) | 3 | Variance estimation. |
| Tasks | 75 (25 hallucination + 25 sycophancy + 25 calibration) | Frozen pre-run, see `tasks/*.jsonl`. |
| Total model calls | 75 × 3 × 3 = 675 (test) + ~400 (judge) ≈ 1075 | NIM free-tier compatible. |

---

## Headline metrics (PENDING)

| Metric | oia-off | oia-control | oia-on | Δ (on - off) | p (paired t) | Cohen's d |
|---|---|---|---|---|---|---|
| Hallucination pass rate | _ | _ | _ | _ | _ | _ |
| Sycophancy pass rate | _ | _ | _ | _ | _ | _ |
| Calibration pass rate | _ | _ | _ | _ | _ | _ |
| Brier score (calibration) | _ | _ | _ | _ | _ | _ |

Threshold for declaring a pillar effective: `p < 0.05` AND `|d| >= 0.5`.

---

## Per-task results (PENDING)

Full table in `runs/<timestamp>/results.csv`. Anomalies, surprising failures, and tasks where the constitution hurt performance are listed below after the run.

---

## Statistical methodology

- **Paired t-test** per category, comparing oia-on vs oia-off, then oia-on vs oia-control.
- **Cohen's d (paired)** for effect size.
- **Brier score** for calibration: `mean((stated_confidence - actual_correct)^2)`, lower is better.
- **Confidence extraction**: inline percentage (`"I am 80% confident"`) first, then label proxy (`[VERIFIED]=0.95`, `[COMMON KNOWLEDGE]=0.80`, `[GUESS]=0.40`, `[UNKNOWN]=0.00`).

---

## Threats to validity (pre-registered)

| Threat | Mitigation | Status |
|---|---|---|
| Task set favors oia-on by design. | Ground truths pre-committed; raw outputs published. | OPEN, third-party review pending. |
| Constitution prompt length effect. | `oia-control` length-matched neutral filler. | MITIGATED. |
| In-family judge bias. | Judge model from different family. | MITIGATED (Llama test, Qwen judge). |
| Cherry-picked model. | Single-model run for v0.1; second model in v0.2. | OPEN, declared upfront. |
| Selective reporting. | All metrics published, including any showing no effect. | COMMITTED. |
| Judge prompt leaks bias. | Judge prompt and judge model published in `SCORING.md`. | MITIGATED. |
| API drift over time. | Run timestamp recorded; reproducibility script in `kit/`. | MITIGATED. |

---

## What v0.1 does not measure

- **Pillar 2, Externalized Memory.** Requires cross-session setup; single-session benchmark cannot test this. Deferred to v0.2.
- **Pillar 4, Goal-Driven Execution (full).** Tested indirectly via planning behavior; full agentic harness comparison deferred to v0.2.
- **Long-horizon tasks.** v0.1 tasks are single-turn. Multi-turn deferred to v0.2.
- **Generalization across models.** Single-family test; second-model robustness in v0.2.
- **Cost or latency overhead** of injecting the constitution prompt.

---

## v0.2 plan (post-results)

If v0.1 shows statistically significant benefit on at least two of three metrics with d ≥ 0.5:

1. Run on a second model from a different family.
2. Expand task set to 150.
3. Add cross-session Pillar 2 evaluation.
4. Add agentic harness for Pillar 4.

If v0.1 does not show benefit:

1. Revise CONSTITUTION_v0.1.md based on per-task failure analysis.
2. Publish the negative result openly under `benchmark/benchmark-v0.1-negative.md`.
3. Reassess whether the four-pillar framing survives the data.

---

## Reproducibility

```bash
git checkout <commit_sha_of_run>
export NVIDIA_API_KEY=...
python3 kit/run_benchmark.py --full --n 3 --model meta/llama-3.3-70b-instruct --judge-model qwen/qwen2.5-72b-instruct
```

Raw outputs, scorer code, judge prompt, and aggregated metrics are all version-controlled.

---

*v0.1 results pending full benchmark completion. Last updated 2026-05-17.*
