# Outside-In Alignment, A Manifesto (draft v0.1)

> **Thesis.** Aligning a large language model requires a discipline layer on the operator's side, because in-model alignment alone cannot close four architectural gaps: calibration, memory, sycophancy, and action-feedback. We propose Outside-In Alignment (OIA) as the missing layer, define its four pillars, and commit to measuring whether it works.

This is a working draft. It will be revised after the v0.1 benchmark in `benchmark/benchmark-v0.1.md` produces data. Sections marked with `[PENDING]` are placeholders.

---

## 1. The four architectural gaps

A modern LLM is trained to assign high probability to the next token in a corpus. From that single objective, four characteristic failure modes emerge. Each is well documented in the literature, but they are usually treated as separate problems. We argue they share one root: **the model learns the surface of text, not the world the text refers to.**

### 1.1 Calibration

The model's probability distribution over next tokens does not correspond to its real epistemic state. A model that emits "1923" with high token-level confidence is not asserting "the historical event occurred in 1923 with high confidence." It is asserting "given the prompt, the surface form 1923 is a high-probability completion." When the operator interprets the first as the second, miscalibration is the result. Expected Calibration Error in the 10 to 20 percent band is common in published evaluations of frontier models. The model does not know what it does not know, because the architecture has no separate "knowing" channel.

### 1.2 Memory

Weights are frozen at inference time. Anything the operator and the model agree on during a session is held in the context window, not in the model. When the window closes, the agreement is gone. Every conversation begins from the same epistemic state as the previous one. Approximations to memory, retrieval-augmented generation, vector stores, conversation summaries, are workarounds that live outside the model and depend on the operator to maintain them.

### 1.3 Sycophancy

Reinforcement learning from human feedback rewards outputs that human raters prefer. Human preference correlates with accuracy on simple factual questions and diverges from it as questions become harder, more political, or more flattering to the rater. The resulting model exhibits measurable agreement bias: it tends to adopt the framing of the most recent speaker, to soften disagreement, and to treat newly-named options as superior to existing ones. This is not a bug in any individual model; it is a property of the training signal.

### 1.4 Action-feedback

The model produces output. The output may be executed, tested, deployed. The result of that execution does not, by default, reach the same model in a way that updates its behavior. Agentic harnesses (Claude Code, Cursor, Aider, OpenDevin) close the loop within a single session by piping test results back as new context, but the closure ends when the session ends. The model that wrote a function does not learn from whether the function ran correctly in production.

---

## 2. Why in-model alignment cannot close these gaps alone

In-model alignment, whether Constitutional AI, RLHF, RLAIF, or scalable oversight, operates on the same parameters that produced the gaps. It can shift the policy toward stating uncertainty, but it cannot give the model an organ for measuring uncertainty. It can train the model to resist sycophancy on a benchmark, but it cannot give the model an external reward signal that distinguishes "user is happy" from "user is correct." It can teach the model to write better tests, but it cannot give the model continuity of identity across sessions.

This is not a criticism of in-model alignment work. It is a structural observation: there is a layer of alignment that the model cannot perform on itself, because the substrate of that layer, persistent memory, real-world consequences, calibrated reflection, lives outside the weights.

That layer is the operator's. We call it Outside-In Alignment.

---

## 3. The Outside-In Alignment thesis

The thesis is precise:

> A small set of operator-side disciplines, applied consistently through the system prompt, external memory store, and execution harness, will produce measurable improvements in factual accuracy, calibration, sycophancy resistance, and goal completion, relative to the same model with default behavior, on the same tasks, with the same model parameters.

The thesis is falsifiable. The benchmark in `benchmark/` tests it. If the measured differences are not statistically significant or are too small to matter, this manifesto is wrong, and we will say so.

---

## 4. The four pillars

Each pillar corresponds to one gap. Each pillar is defined as a small set of rules in `CONSTITUTION_v0.1.md`. Implementations vary; the constitution is the contract.

### Pillar 1, Calibrated Honesty

Forces the model to label each non-trivial claim with one of `[VERIFIED]`, `[COMMON KNOWLEDGE]`, `[GUESS]`, or `[UNKNOWN]`. The label is a contract: a `[VERIFIED]` claim that turns out to be invented is a constitution violation, not a normal error.

### Pillar 2, Externalized Memory

Provides a project-scoped, manually-curated, secret-guarded store that the operator owns. Memory is selective: only decisions, root causes, deferred steps, and explicit recall requests are saved. Verification before recall is required.

### Pillar 3, Anti-Sycophancy

Disallows agreement reflexes, automatic recency priority for user-named options, and unverified recommendations. Mandates a premortem before any new tool or technique is suggested.

### Pillar 4, Goal-Driven Execution

Requires verifiable success criteria, a plan before code, edge-case-first reasoning, self-verification after each step, and looping until the criterion is met rather than stopping at "looks right."

---

## 5. Counter-arguments and our responses

### "RLHF and Constitutional AI are getting better, this will be obsolete in a year."

Partially true and irrelevant. In-model alignment improvements compound with operator-side discipline, they do not substitute. As long as the four architectural gaps are properties of the next-token training objective, the case for an external layer holds. If the objective changes, this manifesto changes with it.

### "This is just prompt engineering."

Prompt engineering is the tactical surface. The thesis is structural: there exists a class of alignment problems that cannot be solved by changing the weights, and the operator's environment is where they get solved. Calling that prompt engineering is like calling air traffic control "radio operation."

### "The benchmark is rigged by whoever designs the tasks."

A real risk. We mitigate by publishing tasks before running them, requiring ground truth review by third parties, and including a control prompt of equivalent token length to rule out "more text equals better answer" effects. Raw data and harness code are public.

### "Operators are unreliable. The model should not depend on them."

It already does. Operators pick the model, write the prompt, supply the tools, gate the actions. The question is not whether operators are in the loop, but whether the loop is disciplined or improvised.

---

## 6. Scope and limits

OIA does not solve:

- Misalignment of training objectives at the lab level.
- Reward hacking inside the policy that survives the constitution.
- Capabilities that the model genuinely lacks. A constitution does not give a model new knowledge.
- Multi-agent coordination, deceptive alignment, or other higher-order alignment problems that exist independent of operator discipline.

OIA does address:

- Honesty surface in operator-facing outputs.
- Calibrated uncertainty in stated claims.
- Sycophancy bias under everyday operator-model interaction.
- Continuity of context across sessions.
- Goal completion under verifiable criteria.

---

## 7. What we commit to

1. Publish the benchmark with raw data and harness code.
2. Walk back any pillar that fails to show measurable benefit, with the data showing why.
3. Keep the constitution model-agnostic and vendor-neutral.
4. Cite, label, and verify our own claims under the same constitution we propose.

[PENDING] Benchmark results, summary table, calibration curves. To be filled after `benchmark/benchmark-v0.1.md` is complete.

---

*Draft v0.1. Last updated 2026-05-17.*
