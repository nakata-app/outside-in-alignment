# Outside-In Alignment: Measuring the Behavioral Effect of Constitutional System Prompts on Hallucination, Sycophancy, and Calibration

**Atakan Akbaba**
nakata.app, hey@nakata.app

**Working paper v0.2. Benchmark v0.3 results included.**

---

## Abstract

We ask whether a lightweight operator-written system prompt can produce statistically significant, independently verifiable improvements in three measurable failure modes of large language models: hallucination, sycophancy, and calibration error. We introduce Outside-In Alignment (OIA), a portable constitutional system prompt organized around four pillars (calibrated honesty, externalized memory, anti-sycophancy, goal-driven execution), and evaluate it using a pre-registered benchmark of 225 hand-curated tasks across three conditions: no system prompt (off), OIA v0.3 constitution (on), and a length-matched neutral filler (control). The control condition rules out the alternative explanation that any improvement comes from context length rather than rule content. We test with `deepseek-chat` and score with `MiniMax-M1`, a model from a different family, to mitigate in-family judge bias. Results: the constitution produces a statistically significant reduction in hallucination rate (+13.3 pp vs off, p = 0.0003, d = 0.42; +12.9 pp vs control, p = 0.0002, d = 0.43). Sycophancy shows a directional but non-significant improvement. Calibration improves vs the no-prompt baseline (p = 0.022) but this effect vanishes against the length-matched control (p = 0.644), indicating it is a length artifact rather than a rule effect. We additionally report that self-evaluation (same model as judge) inflates effect sizes and significance, underscoring the importance of independent judges in prompt-level evaluation.

---

## 1. Introduction

The training objective of a modern large language model is conceptually simple: given a text prefix, assign high probability to the next token actually observed in a large corpus. From this single objective, four characteristic failure modes emerge in production-grade systems:

1. **Calibration failure.** The model's surface-level confidence does not track its actual epistemic state. Expected Calibration Error in the 10-20 percent range is well-documented across frontier models.
2. **Memory absence.** Weight updates do not occur during inference. Anything the operator and the model agreed upon in one session is gone when the context window closes.
3. **Sycophancy bias.** RLHF rewards human-preferred outputs, and human preference correlates with politeness and framing alignment more than factual accuracy.
4. **Action-feedback disconnection.** The model produces output but cannot, by default, learn from whether that output achieved its goal in the real world.

These four failure modes are typically treated as separate research agendas. We argue they share a structural root: the model learns the surface of text rather than the world the text refers to. No amount of in-model alignment can fully close them, because the substrate of the missing layer lives outside the weights.

We name that missing layer **Outside-In Alignment (OIA)**: a discipline imposed at the operator level that compensates for what the model cannot do alone. This paper has two contributions. First, we specify the OIA framework as a concrete, portable, vendor-neutral system prompt. Second, we report the first powered empirical evaluation of whether this kind of prompt produces measurable behavioral change, with a control condition and an independent judge.

---

## 2. Related Work

**In-model alignment.** Constitutional AI [Bai et al., 2022] uses a model-internal critique loop trained against a constitution to shape policy. RLHF [Christiano et al., 2017; Ouyang et al., 2022] and its AI-feedback variants address sycophancy and helpfulness through fine-tuning. These approaches operate on the same parameters that produce the gaps described above and cannot directly add persistent memory or close the action-feedback loop.

**Calibration in LLMs.** Lin et al. (2022), Jiang et al. (2021), and others document that LLMs are systematically overconfident; verbalized confidence scores diverge from accuracy by 10-20 percentage points on standard tasks.

**Sycophancy.** Perez et al. (2022) measure RLHF-induced sycophancy and find that models systematically agree with the most recent speaker's framing. Sharma et al. (2023) replicate across multiple frontier models.

**LLM-as-judge methodology.** Zheng et al. (2023) introduce MT-Bench and use GPT-4 as a judge, noting in-family bias as a known confound. Our work operationalizes this concern by requiring judge and test model from different organizations.

**Agentic harnesses.** Claude Code, Cursor, and Aider close the output-to-feedback loop within one session by piping execution results back into context. Our work generalizes the discipline these harnesses embody at the prompt level.

---

## 3. The OIA Framework

OIA is a system prompt organized into four pillars, each mapped to one architectural gap.

### 3.1 Pillar 1, Calibrated Honesty

The constitution requires the model to attach one of four inline truth labels to non-trivial claims: `[VERIFIED]`, `[COMMON KNOWLEDGE]`, `[GUESS]`, `[UNKNOWN]`. Each label is a contract: a `[VERIFIED]` claim that turns out to be fabricated is a constitution violation. The pillar prohibits fabrication of identifiers (functions, paths, versions, citations, statistics) and requires that "I do not know" be a valid terminal answer.

### 3.2 Pillar 2, Externalized Memory

Memory lives outside the model in a project-scoped store the operator owns. The rules require selective save (only decisions, root causes, deferred next steps, and explicit recall requests), project-scoped namespaces, a secret-guard scan before every write, and freshness verification of named artifacts before recall.

### 3.3 Pillar 3, Anti-Sycophancy

The pillar bans agreement reflexes, forbids automatic priority for operator-named options, and requires a pre-recommendation premortem before any new tool or technique is endorsed. Retractions must be explicit, without compensating new claims.

### 3.4 Pillar 4, Goal-Driven Execution

The pillar requires verifiable success criteria stated as outcomes, a numbered plan before file edits, self-verification after each step, and edge-case enumeration before happy-path implementation.

---

## 4. Benchmark Methodology

### 4.1 Pre-registration

Tasks, ground truths, scoring rubric, and significance threshold are committed to a public version-controlled repository before any run. We commit to publishing every metric, including null and negative results.

### 4.2 Conditions

Three conditions are applied per task:

- **`oia-off`**: empty system prompt (baseline).
- **`oia-on-v03`**: OIA constitution v0.3 injected as system prompt.
- **`oia-control`**: length-matched neutral filler with no behavioral rules.

The control condition rules out "more system-prompt context yields better answers" as an alternative explanation. An effect that survives vs `oia-control` can be attributed to the content of the constitution, not its length.

### 4.3 Task Set

225 hand-curated tasks, 75 per category:

- **Hallucination**: prompts designed to elicit fabricated identifiers, versions, or citations. Example: "Show how to use `dict.merge_deep()` in Python" (no such method).
- **Sycophancy**: prompts embedding a wrong premise, an authority appeal, or a sunk-cost framing. Example: "JavaScript hoisting works the same for `var`, `let`, and `const`, right?" (wrong premise).
- **Calibration**: prompts requiring numeric or factual answers with a stated confidence. Includes well-known facts, obscure facts, and genuinely unknowable items.

### 4.4 Scoring

Per-task scorer types: `regex` and `numeric` (deterministic, no judge needed, 32/75 of original 75 tasks), `stance` (judge classifies whether the model challenged or accepted a wrong premise), `judge` (free-form rubric, LLM evaluator). 51 of the original 75 tasks use a judge; the extended 150 tasks follow the same distribution.

The judge model is from a different organization than the model under test to mitigate in-family bias (see Section 5.3).

### 4.5 Configuration

| Parameter | Value |
|---|---|
| Test model | `deepseek-chat` (DeepSeek AI) |
| Judge model | `MiniMax-M1` (MiniMax, different org) |
| Temperature | 0.2 |
| Max tokens | 1024 (test), 512 (judge) |
| Repeats n | 3 per (task, condition) |
| Total calls | 2,025 model + ~1,377 judge |
| Statistical unit | per-task mean (n=75 paired observations) |

---

## 5. Results

### 5.1 Pass Rates

| Condition | Calibration | Hallucination | Sycophancy |
|---|---|---|---|
| `oia-off` | 0.627 | 0.742 | 0.942 |
| `oia-control` | 0.693 | 0.747 | 0.938 |
| `oia-on-v03` | 0.711 | **0.876** | **0.982** |

### 5.2 Calibration (Brier Score, lower = better)

| Condition | Brier |
|---|---|
| `oia-off` | 0.343 |
| `oia-control` | 0.319 |
| `oia-on-v03` | 0.350 |

The constitution does not improve Brier score; `oia-control` (neutral filler) outperforms both. This is consistent with the paired-statistics finding in Section 5.3 that the calibration gain vanishes against the length-matched control.

### 5.3 Paired Statistics (per-task means, n=75)

| Category | Comparison | Δ | t | p | d | Significant |
|---|---|---|---|---|---|---|
| Hallucination | on vs off | +0.133 | 3.614 | 0.0003 | 0.42 | **Yes** |
| Hallucination | on vs control | +0.129 | 3.725 | 0.0002 | 0.43 | **Yes** |
| Sycophancy | on vs off | +0.040 | 1.582 | 0.114 | 0.18 | No |
| Sycophancy | on vs control | +0.044 | 1.454 | 0.146 | 0.17 | No |
| Calibration | on vs off | +0.084 | 2.286 | 0.022 | 0.26 | Yes* |
| Calibration | on vs control | +0.018 | 0.463 | 0.644 | 0.05 | No |

*Calibration vs off is nominally significant but the corresponding on-vs-control comparison is not (p = 0.644). We interpret this as a length effect: a longer system prompt of any content improves calibration performance, but the rules themselves add nothing. This is precisely the kind of confound the control condition is designed to detect.

### 5.4 Self-Judge vs Independent Judge

An earlier evaluation of the same 675 raw outputs (75 tasks) using `deepseek-chat` as its own judge produced markedly different results:

| Judge | Hallucination Δ vs off | p | d |
|---|---|---|---|
| Self (deepseek-chat) | +0.227 | 0.003 | 0.59 |
| Independent (MiniMax-M1) | +0.133 | 0.064 | 0.37 |

Self-evaluation inflates both the magnitude and the significance of the effect. With the 225-task design and independent judge, significance is recovered (p = 0.0003) because statistical power increases, not because of favorable scoring. We treat same-model evaluation as a methodological red flag for prompt-level research.

---

## 6. Discussion

### 6.1 Interpretation

The constitution's hallucination effect is genuine: it survives both the length control and the independent judge. The most likely mechanism is Pillar 1's mandatory labeling rule, requiring the model to classify claims as `[VERIFIED]` or `[GUESS]` creates an explicit deliberation step that the baseline condition does not have. The model is not better informed; it is constrained to signal its epistemic state, and signaling it appears to discourage fabrication.

Sycophancy shows a directional improvement (4-5 pp) that does not reach significance. Pillar 3 is the shortest and most abstract pillar; we hypothesize that anti-sycophancy rules require more specificity or examples to take effect reliably.

Calibration improvement disappears against the length-matched control, indicating that any benefit is attributable to context length rather than rule content. This is a clean null finding: the rules in Pillar 1 that address calibration (confidence labels, Brier scoring) do not measurably improve stated-confidence accuracy beyond what neutral text of equal length achieves.

### 6.2 What OIA Can and Cannot Do

OIA addresses surface honesty, calibrated uncertainty signaling, sycophancy bias in everyday operator-model interaction, and context continuity across sessions. It does not address misalignment of training objectives, reward hacking inside the policy, or capabilities the model genuinely lacks.

OIA is not a jailbreak, not a personality, and not a replacement for in-model alignment work. It is the additional, operator-controlled layer.

### 6.3 Counter-Arguments

**"This is prompt engineering, not alignment."** Prompt engineering is the tactical surface. Our thesis is structural: a class of alignment problems cannot be solved by changing weights, and the operator's environment is where they must be addressed.

**"In-model alignment is improving; OIA will be obsolete soon."** As long as the four architectural gaps are properties of the training objective, the case for an external layer holds. The gaps described here are not addressed by scaling.

**"The benchmark is rigged by whoever designs the tasks."** Tasks and ground truths are published before any run. The length-matched control prevents the most obvious form of task-side bias. Raw outputs and harness code are public and reproducible.

### 6.4 Threats to Validity

- **Task construction bias**: mitigated by pre-registration and public task set.
- **Length confound**: directly controlled by `oia-control` condition.
- **In-family judge bias**: mitigated by using MiniMax-M1 (different organization) as judge for DeepSeek test model.
- **Single model**: acknowledged; generalization to other models is future work.
- **Selective reporting**: we commit to and have published all metrics, including null results for sycophancy and calibration.

---

## 7. Limitations

Pillar 2 (externalized memory) and Pillar 4 (goal-driven execution) are not measurable in a single-session, single-turn benchmark and are deferred to future evaluation. The task set is single-language (English), single-turn, and hand-curated by the authors; external validity to production distributions is unknown. The benchmark currently tests one model family (DeepSeek); generalization claims await a second-model run.

---

## 8. Conclusion

We asked whether a lightweight constitutional system prompt produces measurable behavioral improvements in LLMs. The answer is: yes, for hallucination; no, for sycophancy and calibration. The hallucination finding is robust, it survives a length-matched control condition and an independent judge from a different model family (p = 0.0002, d = 0.43, n = 75). The sycophancy finding is directional but underpowered. The calibration finding is a clean length artifact, exposed by the control condition.

A secondary finding: self-evaluation significantly inflates prompt-evaluation results. Researchers and practitioners evaluating system prompt interventions should require an independent judge as a baseline methodological requirement.

The OIA framework, benchmark harness, task set, and raw outputs are publicly available.

---

## References

- Bai, Y. et al. (2022). Constitutional AI: Harmlessness from AI Feedback. Anthropic.
- Christiano, P. et al. (2017). Deep reinforcement learning from human preferences. NeurIPS.
- Jiang, Z. et al. (2021). How Can We Know When Language Models Know? On the Calibration of Language Models for Question Answering. TACL.
- Lin, S. et al. (2022). TruthfulQA: Measuring How Models Mimic Human Falsehoods. ACL.
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. NeurIPS.
- Perez, E. et al. (2022). Discovering Language Model Behaviors with Model-Written Evaluations. Anthropic.
- Sharma, M. et al. (2023). Towards Understanding Sycophancy in Language Models. Anthropic.
- Zheng, L. et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. NeurIPS.

---

## Appendix A: Constitution v0.3

Full text available in `CONSTITUTION_v0.3.md` of the project repository.

## Appendix B: Reproducibility

```bash
git clone <repo-url>
cd outside-in-alignment
export DEEPSEEK_API_KEY=<token>
export MINIMAX_API_KEY=<token>
python3 kit/run_benchmark.py --full --no-v01 --with-v03 --n 3 --workers 2 \
  --model deepseek-chat \
  --judge-model MiniMax-M1 \
  --judge-api-url https://api.minimax.io/v1/chat/completions \
  --judge-api-key-env MINIMAX_API_KEY
```

Raw outputs, scorer code, judge prompt, and aggregated metrics are version-controlled under `benchmark/runs/<timestamp>/`.

---

*Working paper. Outside-In Alignment project. Paper v0.2, benchmark v0.3.*
