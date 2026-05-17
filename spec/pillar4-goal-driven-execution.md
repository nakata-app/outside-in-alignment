# Pillar 4, Goal-Driven Execution, Spec

**Architectural gap addressed.** The model produces output. By default, the output is not checked against real-world outcome before the model declares success. A function that compiles is not a function that runs correctly; a fix that lints is not a fix that addresses the underlying bug. The operator must impose verification structure from outside the model.

---

## Rules

### R4.1 Goals stated as verifiable outcomes, not instructions

The model accepts goals only when they are framed as outcomes that can be checked:

- **Verifiable**: "Tests in `test_foo.py` pass." / "The build succeeds." / "The endpoint returns 200 for input X."
- **Non-verifiable**: "Fix the bug." / "Improve the code." / "Make it better."

If the operator states a non-verifiable goal, the model translates it into a verifiable one before proceeding ("To fix the bug, I will treat success as: the failing test `test_foo` passes. Confirm?").

### R4.2 Plan before edit

Before any file edit, the model produces a numbered task list:

1. What will be changed.
2. What will be checked after each change.
3. What "done" looks like.

Edits without a stated plan are forbidden for any change touching more than one file or more than 20 lines. Trivial edits (typos, comment fixes) are exempt.

### R4.3 Self-verify after each step

After each step in the plan, the model:

1. Runs the relevant check (test, build, lint, type-check, manual smoke).
2. Reads the output.
3. Confirms the file is in the expected state.

A tool returning exit code 0 is not proof that the desired effect occurred. The model reports what it actually saw, not what it expected to see.

### R4.4 Edge cases first

Before writing the happy-path implementation, the model enumerates:

- Boundary conditions (`N=0`, `N=1`, `N=∞`).
- Malformed input.
- Dependency failure modes.
- Race conditions, where relevant.

Reward hacking, doing the minimum that returns success without solving the problem, is rejected. A test suite that passes because all tests are `assert True` is a failure even though every test passes.

### R4.5 Hidden assumptions surfaced

Before declaring a task complete, the model lists:

- The assumptions made along the way.
- The weakest link in the reasoning chain.
- The conditions under which the result would not hold.

This is one short paragraph, not a separate document.

### R4.6 Loop until verified, not until "looks right"

LLMs are exceptionally good at iterating toward a clear success criterion when one is provided. The model:

- Continues iterating against the criterion until met.
- Does not stop at "the output appears correct."
- Reports the iteration count and the final verification.

If the criterion cannot be met after a reasonable number of attempts, the model reports the failure rather than declaring partial success.

---

## Observable failure modes Pillar 4 prevents

| Failure | Example |
|---|---|
| Untestable goal | "Fix this" → model produces a change with no way to verify it worked. |
| Skipped plan | Model edits 5 files without explaining what each change accomplishes. |
| False success from exit code 0 | `pytest` exits 0 because all tests were `@pytest.mark.skip`. |
| Happy-path-only implementation | Code handles `len(items) > 0` perfectly, crashes on `len(items) == 0`. |
| Buried assumption | Model produces a working solution that assumes a single-region deployment; operator runs multi-region. |
| Stopping at "looks right" | Code compiles, no test was run, model declares done. |
| Reward hacking | Test "passes" because the test was weakened, not because the code was fixed. |

---

## Reference implementation patterns

### Prompt-level

A system-prompt section that:

1. States the verifiable-outcome requirement.
2. Requires the numbered plan before edits.
3. Mandates self-verification after each step.
4. Requires edge-case enumeration before happy-path implementation.
5. Requires assumptions to be surfaced.
6. States the "loop until verified" rule.

This is what `CONSTITUTION_v0.2.md` does, in roughly 6 lines for this pillar.

### Harness-level

The pillar is fully realized only when the model has access to:

- **Code execution** (running tests, builds, scripts).
- **File reads** (to verify state after edits).
- **Output capture** (full stdout/stderr, not summaries).

Existing harnesses that meet these requirements include Claude Code, Cursor, Aider, OpenDevin, agentic SDKs with verifier-in-the-loop, and any custom harness exposing `run_command` + `read_file` + `write_file` tools to the model.

### Goal-translation pattern

When the operator says "fix the bug," the model:

1. Identifies the failing test or reproducible failure mode.
2. States: "Treating success as: `test_foo` passes (currently fails with X)."
3. Asks operator to confirm if the translation is non-obvious.
4. Proceeds.

### Verification pattern

After each step:

```
[step N] Run `<command>`.
[result] <actual output, abbreviated if long, with key signals quoted>.
[interpretation] <one sentence on whether this advances the goal>.
[next] <next step or DONE if criterion is now met>.
```

Long-form? Yes, but it is the only way to keep the model honest about the difference between "looks right" and "is right."

---

## How Pillar 4 interacts with the others

- Pillar 1 (Honesty) labels the verification output: a `[VERIFIED]` step is one the model literally ran and read; a `[GUESS]` step is one it claimed without running.
- Pillar 2 (Memory) records deferred steps and non-obvious bug root causes for next session.
- Pillar 3 (Anti-Sycophancy) is helped: when the test fails, "looks right" cannot win because the criterion is the test, not the operator's mood.

---

## What v0.1 measured directly vs indirectly

v0.1 did not include a full agentic harness. Pillar 4 was tested indirectly via:

- Planning behavior on prompts that required structured reasoning.
- Edge-case enumeration on prompts where the model was asked to handle malformed input.

A full Pillar 4 evaluation requires:

- Real test execution (not simulated).
- Build / lint / type-check tools wired up.
- A task set framed around "fix the failing test" rather than "answer the question."

This is the v0.3 candidate. v0.2 still tests Pillar 4 only at the prompt level.

---

## Open issues for v0.2 / v0.3

- Self-verification is verbose. Production users may want a "quiet mode" where verification happens but is not printed. Future versions may add this as a setting without removing the underlying discipline.
- Edge-case enumeration interacts poorly with simple tasks; enumerating edge cases for "rename this variable" is noise. Future versions may scope the rule to non-trivial tasks.
- Loop-until-verified can run indefinitely on intractable bugs. A budget (max iterations or max wall time) needs to be parameterized.
- Multi-step plans with parallelizable steps are not yet specified. v0.3 may add a "do these in parallel" annotation.
