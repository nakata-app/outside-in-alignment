# Contributing to Outside-In Alignment

OIA is a working hypothesis, not a finished product. The most valuable contributions sharpen the hypothesis, falsify it cleanly, or extend it honestly.

## What we welcome

- **Benchmark tasks.** New hand-curated tasks for hallucination, sycophancy, calibration categories, with ground truth and scorer config. See `benchmark/tasks/*.jsonl` for format.
- **Replications.** Re-run the benchmark on different models (Mistral, Qwen, GPT-class, open-weight). Report all metrics, including ones that show no effect or hurt.
- **Constitution edits.** Propose tightening or simplifying rules in `CONSTITUTION_v0.2.md`. Any rule change must be accompanied by a benchmark re-run on the affected pillar.
- **Implementation references.** New memory stores, agentic harnesses, or scorer types that demonstrate a pillar in isolation.
- **Negative results.** A task where OIA-on performs worse than OIA-off, with raw output evidence, is more valuable than another positive result.

## What we do not want

- Cherry-picked positive results without a length-matched control condition.
- "OIA improved my LLM" claims without numbers.
- Rule additions that lengthen the constitution without a corresponding benchmark gain. v0.1 → v0.2 cut 55% of length; complexity is a known cost.
- Personal or stylistic flavor in the constitution. OIA is vendor-neutral, model-agnostic, language-neutral. Stylistic choices live outside.

## Issue and PR conventions

- File an issue before a large PR. State the hypothesis and the measurement that would falsify it.
- Include raw benchmark outputs in `benchmark/runs/<timestamp>/` for any quantitative claim.
- Document threats to validity for any new task category.
- Pre-register significance thresholds before running the benchmark; do not adjust them after seeing results.

## Code style

- Python 3.10+, stdlib-only where reasonable. The benchmark harness is intentionally dependency-free.
- One commit, one logical change.
- Truthful commit messages. If a commit ships an untested hack, say so.

## Honesty bar

Under the same constitution we propose: if you publish a result, label your epistemic state. If you do not know, say so. If a tool failed, say it failed. Selective framing and silent rounding are constitution violations.

## License

By contributing, you agree your work is released under the MIT license in `LICENSE`.
