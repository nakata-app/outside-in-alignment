# Outside-In Alignment (OIA)

> An operator-side discipline layer for LLMs. Closes four architectural gaps that in-model alignment alone cannot reach: calibration, memory, sycophancy, and action-feedback.

**Status: v0.1, pre-benchmark.** The thesis is stated. The numbers are not yet in. This README will be updated when `benchmark/benchmark-v0.1.md` produces data.

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
CONSTITUTION_v0.1.md   The rule set, drop into any LLM system prompt.
docs/MANIFESTO_draft.md  The argument behind the rules.
spec/four-pillars.md   Per-pillar implementation spec.
benchmark/             A/B harness, task set, and results. v0.1 in preparation.
kit/                   CLI tool to install the constitution into any project. v0.1 in preparation.
paper/                 Technical report, arXiv-style. v0.1 in preparation.
```

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

If the benchmark fails to show benefit, the thesis is wrong in its current form and will be revised or withdrawn.

---

## License

MIT. See `LICENSE`.

## Contributing

Issues and pull requests welcome once the v0.1 benchmark is published. Until then, the constitution and the manifesto are open for review and critique.
