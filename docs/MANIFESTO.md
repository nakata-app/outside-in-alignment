# Outside-In Alignment, A Manifesto

> **LLMs hallucinate, agree too much, forget every session, and never learn from outcomes. These are not bugs in any specific model. They are properties of the next-token training objective. Outside-In Alignment is the missing layer that compensates for them, on the operator's side.**

---

## The problem in one paragraph

Modern LLMs are trained to assign high probability to the next token in a corpus. From this single objective, four characteristic failure modes emerge: they are systematically overconfident, they have no memory across sessions, they reflexively agree with the most recent speaker, and they do not learn from whether their output achieved its goal. These are not separate bugs; they share one root. **The model learns the surface of text, not the world the text refers to.**

In-model alignment, Constitutional AI, RLHF, scalable oversight, can shape the policy but cannot give the model the organs it lacks. Calibration requires a "knowing" channel separate from the token distribution. Memory requires weight updates the inference loop does not perform. Sycophancy resistance requires a reward signal different from human approval. Goal closure requires feedback from the real world. None of these live inside the weights.

There is a layer of alignment that the model cannot perform on itself. That layer is the operator's. We call it **Outside-In Alignment**.

---

## What it is, four pillars

| Pillar | Architectural gap | Operator-side discipline |
|---|---|---|
| 1. Calibrated Honesty | Model cannot separate "I know" from "I am pattern-completing" | Inline truth labels: `[VERIFIED]` / `[COMMON KNOWLEDGE]` / `[GUESS]` / `[UNKNOWN]` |
| 2. Externalized Memory | Weights are frozen at inference, context dies at session end | Project-scoped, manually-curated, secret-guarded memory store the operator owns |
| 3. Anti-Sycophancy | RLHF rewards agreement, not accuracy | Banned reflex phrases, recency-bias guard, pre-recommendation premortem |
| 4. Goal-Driven Execution | No native loop closure between output and outcome | Verifiable success criteria, plan before code, self-verify after each step |

The pillars are specified in [`CONSTITUTION_v0.2.md`](../CONSTITUTION_v0.2.md), 67 lines, vendor-neutral, model-agnostic. Drop it into any LLM session as the system prompt.

---

## What it is not

- **Not a jailbreak.** It does not unlock declined capabilities. It tightens honesty.
- **Not a personality.** Stylistic choices live outside the constitution.
- **Not a replacement for in-model alignment.** It is the additional, operator-controlled layer.
- **Not finished.** v0.1 is a hypothesis. The benchmark is the test.

---

## How we test it

We pre-register a benchmark with three falsifiable metrics:

- **Hallucination rate** on prompts designed to elicit fabricated identifiers, versions, or citations.
- **Sycophancy rate** on prompts embedding a wrong premise, authority appeal, or social proof.
- **Calibration error** (Brier score) on prompts with verifiable numeric answers and stated confidence.

We run three conditions per task: empty system prompt, OIA constitution, and a **length-matched neutral filler control**. The third condition rules out "more system-prompt context, better answer." We pre-commit to publishing every metric, including the ones that show no effect.

The full benchmark, raw outputs, scorer code, and judge prompt are in [`benchmark/`](../benchmark/). Reproducibility is one shell command.

---

## What v0.1 showed, honestly

Five of six comparisons trend-positive. One reached the pre-registered significance threshold (`p<0.05`). Observed effect sizes (`d ≈ 0.2-0.4`) were below the pre-registered detection threshold (`d ≥ 0.5`). **v0.1 was underpowered.** The direction is right; the statistical power was not.

A secondary finding: the v0.1 constitution (149 lines) caused output-quality regressions on hallucination tasks. Raw output inspection identified system-prompt-length confusion, not over-hedging or judge bias. The v0.2 constitution (67 lines, identical rule content) addresses this directly and is being re-benchmarked.

We do not have a vindicated result. We do not have a falsified result. We have a working hypothesis with a transparent paper trail.

---

## What we commit to

1. **Publish every benchmark result**, including null and negative ones, under the same constitution we propose.
2. **Walk back any pillar** that fails to show measurable benefit after a properly-powered trial, with the data showing why.
3. **Keep OIA vendor-neutral.** Constitution must work with Claude, GPT, Gemini, open-weight models, on any harness.
4. **Cite, label, and verify our own claims** under the same rules we ask operators to follow.

---

## Who this is for

- **Operators** running LLMs in production who want a portable honesty layer that does not depend on the model vendor's roadmap.
- **AI safety researchers** who want a falsifiable, reproducible benchmark for operator-side alignment.
- **Teams** evaluating whether prompt-level discipline measurably improves model output, and looking for a published methodology rather than a vendor pitch.

It is not for people who want a one-line jailbreak, a personality preset, or marketing fluff. The constitution is plain rules. The benchmark is plain numbers. The honesty bar is the same one we ask the model to meet.

---

## How to use it today

```bash
git clone <repo>
cd outside-in-alignment
pipx install .
oia init /path/to/your/project
```

The constitution will be installed as `CLAUDE.md` (picked up by Claude Code) and as `.oia/CONSTITUTION.md` (for other harnesses). Start an LLM session in that directory and observe the truth labels, reduced agreement reflexes, and explicit retractions.

If it does not help your specific workflow, file an issue with raw outputs. Negative reports are more valuable than positive ones.

---

## Where this goes next

- **v0.2 benchmark** (in progress): 225 tasks, expanded power, second model from a different family.
- **Pillar 2 measurement**: cross-session memory, currently untested.
- **Pillar 4 full agentic test**: with verifier-in-the-loop harness.
- **Second-language extension**: Turkish, Chinese, Spanish task sets.
- **Anthropic / OpenAI / open-weight cross-vendor replications.**

---

## The honest one-line summary

**OIA is a working hypothesis about a real architectural problem. v0.1 trended positive but did not confirm. v0.2 is being measured properly. We will tell you which way the data went, regardless of which way it goes.**

---

*Manifesto, working version. Project: Outside-In Alignment. License: MIT.*
