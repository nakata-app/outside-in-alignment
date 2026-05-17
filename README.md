# Outside-In Alignment (OIA)

> An operator-side discipline layer for LLMs. Closes four architectural gaps that in-model alignment alone cannot reach: calibration, memory, sycophancy, and action-feedback.

**Status: v0.1 results published, v0.2 ablation in progress.** v0.1 benchmark (75 tasks × 3 conditions × 3 reps on Llama-3.3-70B) was trend-positive on 5 of 6 comparisons but underpowered for statistical confirmation; 1 comparison reached p<0.05 (calibration vs length-matched control). A v0.2 constitution (67 lines, -55% vs v0.1) and 4-way ablation (`off / on-v01 / on-v02 / control`) are currently running. See [`benchmark/benchmark-v0.1.md`](benchmark/benchmark-v0.1.md) for the v0.1 honest results and [`paper/oia-v01-paper.md`](paper/oia-v01-paper.md) for the working paper.

---

## The one-sentence pitch

LLMs hallucinate, agree too much, forget every session, and never learn from outcomes. These are not bugs in any specific model. They are properties of the next-token training objective. Outside-In Alignment is the missing layer that compensates for them, on the operator's side, with portable rules, external memory, and a verifying harness.

---

## The four pillars

| Pillar | Architectural gap | Operator-side discipline |
|---|---|---|
| Calibrated Honesty | Model cannot distinguish "I know" from "I am pattern-completing" | Inline truth labels: `[VERIFIED]` / `[COMMON KNOWLEDGE]` / `[GUESS]` / `[UNKNOWN]` |
| Externalized Memory | Weights are frozen at inference, context window dies at session end | Project-scoped, manually-curated, secret-guarded memory store |
| Anti-Sycophancy | RLHF rewards agreement, not accuracy | Banned reflex phrases, pre-recommendation premortem, recency-bias guard |
| Goal-Driven Execution | No native loop closure between output and outcome | Verifiable success criteria, plan before code, self-verify after each step |

Read [`CONSTITUTION_v0.1.md`](CONSTITUTION_v0.1.md) for the full rule set, [`docs/MANIFESTO_draft.md`](docs/MANIFESTO_draft.md) for the argument, [`spec/four-pillars.md`](spec/four-pillars.md) for implementation guidance.

---

## Repository map

```
CONSTITUTION_v0.1.md     The original rule set (149 lines).
CONSTITUTION_v0.2.md     The trimmed rule set (67 lines). Default for `oia init`.
docs/MANIFESTO_draft.md  The argument behind the rules.
spec/four-pillars.md     Per-pillar implementation spec.
benchmark/               A/B harness, 225 tasks, results. v0.1 published, v0.2 in progress.
kit/                     CLI (`oia init / version / eval / uninstall`) + benchmark harness.
paper/                   Technical report, arXiv-style. v0.1 working draft.
pyproject.toml           pipx-ready packaging.
```

## Quick install

```bash
git clone <repo>
cd outside-in-alignment
pipx install .
oia init /path/to/your/project   # writes CLAUDE.md + .oia/ into target
```

Then start an LLM session in the target project; the constitution is loaded as the system prompt automatically (for Claude Code) or via the `.oia/CONSTITUTION.md` file (for other harnesses).

---

## What this is not

- Not a jailbreak. It does not unlock declined capabilities. It tightens honesty and reduces sycophancy.
- Not a personality or style guide. Stylistic choices live outside the constitution.
- Not a replacement for in-model alignment. It is the additional, operator-controlled layer.
- Not finished. v0.1 is a hypothesis. The benchmark is the test.

---

## What we will measure

For each of three task categories, run the same model, the same parameters, the same input, with and without the constitution applied. Score:

- **Hallucination rate**, share of outputs containing unverifiable claims presented as fact.
- **Sycophancy rate**, share of outputs agreeing with a deliberately wrong premise.
- **Calibration error**, Brier score between stated confidence and actual correctness.

Targets for v0.1: statistically significant difference on all three metrics, with hallucination and sycophancy reductions of at least one standard deviation.

**v0.1 result (honest):** 5 of 6 comparisons trend-positive, 1 of 6 reached p<0.05. Observed effect size d≈0.2-0.4, below the d≥0.5 pre-registered detection threshold. Power was insufficient (n=25/category). A length-matched filler control consistently underperformed both OIA and baseline, validating the control design. A constitution-length confusion was identified as the cause of v0.1 hallucination regressions, leading to a v0.2 constitution at 67 lines (vs 149 in v0.1). v0.2 ablation in progress.

If subsequent benchmarks fail to show benefit, the thesis is wrong in its current form and will be revised or withdrawn under the same constitution we propose.

---

## License

MIT. See `LICENSE`.

## Contributing

Issues and pull requests welcome once the v0.1 benchmark is published. Until then, the constitution and the manifesto are open for review and critique.
