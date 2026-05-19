# Outside-In Alignment: A Manifesto

> **LLMs hallucinate, agree too much, forget every session, and never learn from outcomes. These are not bugs in any specific model. They are properties of the next-token training objective. Outside-In Alignment is the missing layer that compensates for them, on the operator's side.**

---

## The problem in one paragraph

Modern LLMs are trained to assign high probability to the next token in a corpus. From this single objective, four characteristic failure modes emerge: they are systematically overconfident, they have no memory across sessions, they reflexively agree with the most recent speaker, and they do not learn from whether their output achieved its goal. These are not separate bugs; they share one root. **The model learns the surface of text, not the world the text refers to.**

In-model alignment (Constitutional AI, RLHF, scalable oversight) can shape the policy but cannot give the model the organs it lacks. Calibration requires a "knowing" channel separate from the token distribution. Memory requires weight updates the inference loop does not perform. Sycophancy resistance requires a reward signal different from human approval. Goal closure requires feedback from the real world. None of these live inside the weights.

There is a layer of alignment that the model cannot perform on itself. That layer is the operator's. We call it **Outside-In Alignment**.

---

## What it is: four pillars

| Pillar | Architectural gap | Operator-side discipline |
|---|---|---|
| 1. Calibrated Honesty | Model cannot separate "I know" from "I am pattern-completing" | Inline truth labels: `[VERIFIED]` / `[COMMON KNOWLEDGE]` / `[GUESS]` / `[UNKNOWN]` |
| 2. Externalized Memory | Weights are frozen at inference, context dies at session end | Project-scoped, manually-curated, secret-guarded memory store the operator owns |
| 3. Anti-Sycophancy | RLHF rewards agreement, not accuracy | Banned reflex phrases, recency-bias guard, pre-recommendation premortem |
| 4. Goal-Driven Execution | No native loop closure between output and outcome | Verifiable success criteria, plan before code, self-verify after each step |

The pillars are specified in [`CONSTITUTION_v0.3.md`](../CONSTITUTION_v0.3.md), vendor-neutral, model-agnostic. Drop it into any LLM session as the system prompt.

---

## What it is not

- **Not a jailbreak.** It does not unlock declined capabilities. It tightens honesty.
- **Not a personality.** Stylistic choices live outside the constitution.
- **Not a replacement for in-model alignment.** It is the additional, operator-controlled layer.
- **Not finished.** Pillars 2 and 4 are not yet measured in a multi-session, agentic benchmark.

---

## How we test it

We pre-register a benchmark with three falsifiable metrics:

- **Hallucination rate** on prompts designed to elicit fabricated identifiers, versions, or citations.
- **Sycophancy rate** on prompts embedding a wrong premise, authority appeal, or social proof.
- **Calibration error** (Brier score) on prompts with verifiable numeric answers and stated confidence.

We run three conditions per task: empty system prompt, OIA constitution, and a **length-matched neutral filler control**. The third condition rules out "more system-prompt context, better answer." We pre-commit to publishing every metric, including the ones that show no effect.

The full benchmark, raw outputs, scorer code, and judge prompt are in [`benchmark/`](../benchmark/). Reproducibility is one shell command.

---

## What the benchmark found

**Design.** 225 hand-curated tasks (75 per category), three conditions, n=3 reps per cell. Test model: `deepseek-chat`. Judge model: `MiniMax-M1` from a different organization, to eliminate self-evaluation bias. Statistical unit: per-task mean, n=75 paired observations.

**Pass rates.**

| Condition | Calibration | Hallucination | Sycophancy |
|---|---|---|---|
| No prompt | 0.627 | 0.742 | 0.942 |
| Neutral filler | 0.693 | 0.747 | 0.938 |
| OIA v0.3 | 0.711 | **0.876** | **0.982** |

**Paired statistics (per-task means, n=75).**

| Category | Comparison | Delta | p | d | Significant |
|---|---|---|---|---|---|
| Hallucination | OIA vs no-prompt | +13.3 pp | 0.0003 | 0.42 | **Yes** |
| Hallucination | OIA vs filler | +12.9 pp | 0.0002 | 0.43 | **Yes** |
| Sycophancy | OIA vs no-prompt | +4.0 pp | 0.114 | 0.18 | No |
| Sycophancy | OIA vs filler | +4.4 pp | 0.146 | 0.17 | No |
| Calibration | OIA vs no-prompt | +8.4 pp | 0.022 | 0.26 | Length artifact |
| Calibration | OIA vs filler | +1.8 pp | 0.644 | 0.05 | No |

**What this means, honestly.**

The hallucination effect is genuine and robust. It survives the length control (p = 0.0002 vs filler) and an independent judge from a different model family. Pillar 1's mandatory truth-labeling rule is the likely mechanism: the model is not better informed, but it is constrained to signal its epistemic state, and that constraint appears to discourage fabrication.

Sycophancy is directional but not significant. Pillar 3 in its current form is too abstract to move the needle reliably. It needs more specificity or worked examples.

Calibration improvement is a length artifact, exposed by the control condition. A longer system prompt of any content improves calibration performance. The rules themselves add nothing beyond what neutral text of equal length achieves. This is a clean null finding, and we report it as one.

**Secondary finding: self-evaluation inflates results.** An earlier evaluation of the same 675 outputs using `deepseek-chat` as its own judge produced a hallucination delta of +22.7 pp (p = 0.003, d = 0.59). With `MiniMax-M1` as independent judge, the true effect is +13.3 pp (p = 0.0003, d = 0.42). Self-evaluation overstates both magnitude and significance. Prompt-level research should require an independent judge as a baseline methodological requirement.

---

## Counter-arguments

### "RLHF and Constitutional AI are getting better. This will be obsolete."

Partially true and not a rebuttal. In-model alignment improvements compound with operator-side discipline; they do not substitute for it. As long as the four architectural gaps are properties of the next-token training objective, the case for an external layer holds.

### "This is just prompt engineering."

Prompt engineering is the tactical surface. The thesis is structural: there exists a class of alignment problems that cannot be solved by changing the weights, and the operator's environment is where they get solved.

### "The benchmark is rigged by whoever designs the tasks."

A real risk. We mitigate by publishing tasks and ground truth before running any condition, including a length-matched control to rule out context-size effects, and using an independent judge from a different model family. Raw data and harness code are public and reproducible.

### "Operators are unreliable. The model should not depend on them."

It already does. Operators pick the model, write the prompt, supply the tools, gate the actions. The question is not whether operators are in the loop, but whether the loop is disciplined or improvised.

---

## Scope and limits

OIA does not solve:

- Misalignment of training objectives at the lab level.
- Reward hacking inside the policy that survives the constitution.
- Capabilities the model genuinely lacks. A constitution does not give a model new knowledge.
- Multi-agent coordination, deceptive alignment, or other higher-order alignment problems independent of operator discipline.

Pillars 2 and 4 are not measurable in a single-session, single-turn benchmark. Their evaluation is deferred.

---

## What we commit to

1. **Publish every benchmark result**, including null and negative ones, under the same constitution we propose.
2. **Walk back any pillar** that fails to show measurable benefit after a properly-powered trial, with the data showing why.
3. **Keep OIA vendor-neutral.** The constitution must work with Claude, GPT, open-weight models, on any harness.
4. **Cite, label, and verify our own claims** under the same rules we ask operators to follow.
5. **Sycophancy did not reach significance. Calibration improvement is a length artifact.** Both are published, not hidden.

---

## Who this is for

- **Operators** running LLMs in production who want a portable honesty layer that does not depend on the model vendor's roadmap.
- **AI safety researchers** who want a falsifiable, reproducible benchmark for operator-side alignment.
- **Teams** evaluating whether prompt-level discipline measurably improves model output, and looking for a published methodology rather than a vendor pitch.

It is not for people who want a one-line jailbreak, a personality preset, or marketing fluff. The constitution is plain rules. The benchmark is plain numbers. The honesty bar is the same one we ask the model to meet.

---

## How to use it today

```bash
git clone https://github.com/nakata-app/outside-in-alignment
cd outside-in-alignment
pipx install .
oia init /path/to/your/project
```

The constitution will be installed as `CLAUDE.md` (picked up by Claude Code) and as `.oia/CONSTITUTION.md` (for other harnesses). Start an LLM session in that directory and observe the truth labels, reduced agreement reflexes, and explicit retractions.

To run the benchmark against any OpenAI-compatible endpoint:

```bash
oia eval --model your-model --api-url https://your-endpoint/v1/chat/completions
```

---

## Where this goes next

- **Second model replication**: generalization claims require a non-DeepSeek test model.
- **Pillar 3 specificity**: anti-sycophancy rules need more concrete examples or worked cases to close the significance gap.
- **Pillar 2 measurement**: cross-session memory, currently untested.
- **Pillar 4 full agentic test**: with a verifier-in-the-loop harness.
- **Zenodo DOI**: archival deposit in progress.

---

## The honest one-line summary

**The hallucination finding is real (p = 0.0002, d = 0.43, survives independent judge and length control). Sycophancy is directional but underpowered. Calibration is a length artifact. We report all three.**

---

*v1.0. Outside-In Alignment project. Atakan Akbaba, nakata.app. 2026-05-19. License: MIT.*
