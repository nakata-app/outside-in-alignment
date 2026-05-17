# Changelog

All notable changes to Outside-In Alignment.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased], v0.2 in progress

### Added
- `CONSTITUTION_v0.2.md` (67 lines, 64% shorter than v0.1) preserving rule content with examples and meta-commentary removed.
- Four-condition benchmark harness: `oia-off`, `oia-on-v01`, `oia-on-v02`, `oia-control`.
- Per-task-mean aggregation for paired statistics (fixes v0.1 paired-stats bug).
- 150 new benchmark tasks (50 per category), bringing total to 225.
- `kit/oia.py` CLI: `init`, `version`, `eval`, `uninstall`.
- `pyproject.toml` for pipx-ready installation.
- `paper/oia-v01-paper.md` working paper (arXiv-style, 226 lines).
- `docs/MANIFESTO.md` final manifesto (product-tone, 113 lines).
- `CONTRIBUTING.md`, honesty bar and contribution rules.
- Per-pillar specification documents in `spec/`: Pillar 1 (calibrated honesty), Pillar 2 (externalized memory), Pillar 3 (anti-sycophancy), Pillar 4 (goal-driven execution).
- `examples/README.md` with real before/after responses from v0.1 benchmark runs.
- GitHub Actions CI: task JSONL validation, harness import check, CLI round-trip, package build, secret-pattern leak scan.

### Changed
- Harness retry behavior: attempts 3 → 6, exponential backoff base 2s → 4s, capped at 180s, added 0.8s inter-call sleep to reduce NIM free-tier 429 rate-limit hits.
- HTTP timeout 120s → 180s.
- README updated with v0.1 results and v0.2 progress.

### Fixed
- Paired-stats computation in `kit/run_benchmark.py` was returning empty results when conditions had different completion counts. Now aggregates per-task-mean before pairing, surviving missing data points.
- `datetime.utcnow()` deprecation warnings replaced with `datetime.now(timezone.utc)`.

## [0.1.0], 2026-05-17

### Added
- `CONSTITUTION_v0.1.md` (149 lines): four pillars (calibrated honesty, externalized memory, anti-sycophancy, goal-driven execution) with rules, operating protocols, and reference implementations.
- `docs/MANIFESTO_draft.md`: argument behind the rules, four architectural gaps thesis.
- `spec/four-pillars.md`: per-pillar implementation spec.
- `benchmark/`: A/B harness with 75 hand-curated tasks (25 per category), three conditions (`oia-off`, `oia-on`, `oia-control` length-matched filler), n=3 repeats per (task, condition).
- `benchmark/SCORING.md`: six scorer types (regex, numeric, label_present, label_correct, stance, judge).
- `benchmark/benchmark-v0.1.md`: pre-registered metrics and significance thresholds, then results.
- Reproducibility commitment: raw model outputs saved under `benchmark/runs/<timestamp>/`, scorer code committed.

### Initial findings
- Five of six on-vs-off and on-vs-control comparisons trend-positive.
- One comparison reached the pre-registered significance threshold: calibration vs length-matched control (p=0.046, d=0.40).
- Observed effect sizes (d ≈ 0.2-0.4) below pre-registered detection threshold (d ≥ 0.5). v0.1 was underpowered.
- Hallucination regression in `oia-on` for v0.1 traced to system-prompt-length confusion on `meta/llama-3.3-70b-instruct`, not over-hedging or judge bias. Diagnosis informed the v0.2 constitution trim.

### Reproducibility
- Single-file harness (`kit/run_benchmark.py`), stdlib-only, Python 3.10+.
- Configuration locked pre-run; task set, ground truths, scorer rubric committed.
- Threats to validity pre-registered.
