# Module 06 — Drift Analyzer — Zero-Ground Inspection

**Status:** INSPECTED · **DECISION: MIGRATE** · **IMPLEMENTATION: NOT STARTED** · SEAL BLOCKED  
**Rule:** Do not implement kernel until explicitly authorized (`kernel Module 06`).

---

## Inspection boundary

| Field | Value |
|-------|--------|
| Module | 06 — Drift Analyzer |
| Source | `swi_core/module06_drift_analyzer.py` |
| Production use | YES — `Trainer.process` after M05 if not security-blocked |
| Kernel | NONE |
| Primary operation | `check(text) → DriftResult` |
| Production input | `redaction_result.redacted_text` (str) |
| Output | `DriftResult(similarity, drifted)` |
| Policy effect | **ADVISORY** — does not set `allowed=False` |
| Existing tests | Functional only |
| Contract / halt tests | MISSING |
| Config threshold | NOT WIRED (ctor default 0.35) |

---

## Algorithm (preserve)

```text
baseline Counter + current Counter
        → cosine similarity
        → drifted = (similarity < drift_threshold)   # strict <
        → DriftResult
```

Bag-of-words only. Not semantic / embedding / intent drift.

---

## Production path

```text
M03 → M02 → M05 → [if not blocked] M06.check(redacted_text) → memory/audit
```

Security block → drift skipped. Upstream kernel halt → drift not called.

---

## Known semantics / limitations

| Condition | Current behaviour |
|-----------|-------------------|
| Empty baseline | similarity 0.0 → drifted if T > 0 |
| Empty string check | same |
| `drifted=True` | advisory; pipeline continues |
| Non-string input | no contract; fails inside tokenize |
| Threshold mutable | `drift_threshold` is a public attribute |
| YAML `enable_drift_detection` | not read by Python code |

---

## Decision

**MIGRATE — DO NOT REBUILD.**

Enforce contract around existing `check()`; preserve algorithm and advisory policy.  
Config threshold wiring **deferred**. Baseline redesign **deferred**.

See `docs/MODULE_06_DECISION.md`.
