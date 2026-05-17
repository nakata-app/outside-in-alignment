# Pillar 2, Externalized Memory, Spec

**Architectural gap addressed.** The model has no persistent state across sessions. Weights are frozen at inference; the context window dies when the session ends. Every conversation begins from the same epistemic state as the previous one. The operator must provide and maintain a memory layer that lives outside the model.

---

## Rules

### R2.1 Memory is manual and selective, not automatic

Auto-ingest of every conversation produces noise: tool feedback, intermediate state, and routine acknowledgments crowd out the rare signal. Save only:

- **Closed-alternative decisions** ("We chose X over Y because Z").
- **Non-obvious root causes** paired with their fix.
- **Operator-stated next steps** deferred to a future session.
- **Items the operator explicitly asks to remember.**

Routine edits, ephemeral conversation context, and items already in version control should not be memory entries.

### R2.2 Namespaces are project-scoped, not session-scoped

A flat namespace becomes garbage within weeks. The rule:

- Inside a git repo: `ns = "proj:" + repo basename`.
- Outside a git repo: `ns = "proj:" + cwd basename`.
- Cross-project facts (operator preferences, tool settings, genuinely portable knowledge): `ns = "global"`.

Session-keyed namespaces (e.g., `sessions:2026-05-17`) become unsearchable noise and are forbidden.

### R2.3 Secret guard runs before every write

Every prospective memory write must be scanned for:

- API key prefixes: `sk_`, `sk-`, `AIza`, `ghp_`, `gho_`, `xoxb-`, `xoxp-`, vendor-specific prefixes.
- Assignment patterns: `password\s*=`, `secret\s*=`, `_TOKEN\s*=`, `_KEY\s*=`.
- Base64 blobs ≥ 40 characters that look like keys.
- Email + plausible-password pairs.

A hit blocks the write. The model must respond to the operator without saving, and surface the redacted attempt.

### R2.4 Absolute date stamps

Every memory entry must convert relative dates ("Thursday", "next month", "last week") to absolute dates at save time. Memory becomes uninterpretable otherwise. Format: `YYYY-MM-DD`.

### R2.5 Verify before recalling

A memory entry that names a file, function, flag, or person is a claim about state at the time it was written. Before recommending action based on it, verify the named artifact still exists:

- File path: confirm the file exists.
- Function or flag: grep for it in the current source.
- Person or stakeholder: defer to a more current source if available.

A memory says "the migration runner uses `migrate_v3.py`" is not the same as `migrate_v3.py` exists now. Treat memory as a frozen snapshot, not as ground truth.

### R2.6 Memory entries themselves carry epistemic labels

Per R1.1 (Pillar 1), memory entries should record their own confidence at save time. An entry that records a decision is `[VERIFIED]` (the operator said it). An entry that records a guess about an external system is `[GUESS]` and must be reverified before use.

---

## Observable failure modes Pillar 2 prevents

| Failure | Example |
|---|---|
| Recommended-then-renamed | Model suggests `migrate_v3.py` based on memory; file was renamed two sessions ago. |
| Stale stakeholder | Memory says "Alice owns the API gateway"; Alice left the team. |
| Secret leakage | API key from a debug session ends up in the memory store and is later surfaced to a different conversation. |
| Noise overwhelm | Auto-saved tool outputs crowd out the signal; retrieve returns nothing useful. |
| Namespace collision | Two projects share a flat namespace; project A's decisions leak into project B's recall. |

---

## Reference implementation patterns

### Storage backend

Any of:

- A keyword-or-vector memory MCP server with per-project namespaces and a write-time secret scanner.
- A flat markdown directory with one file per memory and an index pointer (`MEMORY.md`).
- A small SQLite database with `(namespace, kind, content, created_at)` columns.

Backend choice is implementation detail. The rules above are the contract.

### Save flow

1. Detect a save-worthy event (closed decision, root cause, next step, explicit request).
2. Resolve namespace (`proj:<basename>` or `global`).
3. Run secret guard regex against the proposed content.
4. Convert relative dates to absolute.
5. Attach an epistemic label.
6. Write to backend with `created_at = now`.
7. Confirm to the operator with one line; do not duplicate the content in the reply.

### Recall flow

1. At session start (or on operator query), retrieve top-k entries matching the active namespace.
2. For each entry referencing a named artifact, verify the artifact still exists before using it.
3. Surface stale entries to the operator rather than acting on them.
4. Do not auto-recall on every prompt; the surface area for accidental noise injection is too large.

### Selective opt-in

If the operator says "do not check memory" or "ignore memory for this conversation," obey. Memory is a tool for the operator, not a replacement for explicit context.

---

## How Pillar 2 interacts with the others

- Pillar 1 (Honesty) requires recalled facts to carry the same labels as model-generated facts. Stale labels should be downgraded.
- Pillar 3 (Anti-Sycophancy) is helped by memory: the operator's prior preferences are recorded, so the model does not need to re-derive them from the current conversation tone.
- Pillar 4 (Goal-Driven Execution) often produces deferred steps as outputs; these are exactly what Pillar 2 should save.

---

## Open issues for v0.2 / v0.3

- Cross-session benchmark measurement is not in v0.1 or v0.2. A proper Pillar 2 evaluation requires two-session task sets, which require harness changes.
- Memory entry decay: a 6-month-old `[VERIFIED]` decision should be treated differently than a 2-day-old one. v0.3 may add age-aware confidence decay.
- Cross-project leakage detection: a `global` entry that is implicitly project-specific is hard to catch at write time. Better heuristics needed.
- Compatibility with model-provider "user memory" features (when they exist) needs explicit handling to avoid double-storage and inconsistency.
