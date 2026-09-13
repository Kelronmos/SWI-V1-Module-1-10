# Module 06 — Kernel Migration Procedure

**Status:** READY for execution · **IMPLEMENTATION: NOT EXECUTED** · **SEAL: BLOCKED**

Decision: **MIGRATE** (do not rebuild). See `docs/MODULE_06_DECISION.md`.

---

## Objective

Smallest change that places existing `DriftAnalyzer.check()` behind `ModuleKernel` without changing what M06 means:

```text
str → tokenize → vectorize → cosine → (similarity < T) → DriftResult
```

**Preserve:** algorithm helpers, `set_baseline` replace semantics, default T=0.35, strict `<`, advisory `drifted`, empty-baseline → sim 0 / drifted when T>0, production input = M05 redacted text.

**Do not:** embeddings, drift-driven halt, config threshold wiring (deferred), silent empty-baseline “fix”.

---

## Contract (to implement)

| Layer | Rule |
|-------|------|
| Pre | `text` is `str` |
| Op | existing `_check` body |
| Post | `DriftResult`; `similarity` finite float; prefer \[0,1\] with documented tolerance if needed; `drifted` is `bool` |
| Ctor (optional this migration) | finite threshold; prefer `0 ≤ T ≤ 1` only with tests |
| Failure | `ModuleKernelError` — not disguised as `DriftResult` |
| Policy | `drifted=True` does **not** halt / does **not** set `allowed=False` |

---

## Implementation order

1. Baseline green (existing M06 tests)  
2. Kernel-wrap `check()`  
3. Direct contract tests  
4. Trainer halt + downstream not reached  
5. M05→M06 redacted-input regression  
6. Full suite + `verify.sh`  
7. Commit complete tip (avoid intermediate-only seal)  
8. CI green  
9. Seal record with run ID + SHA  

---

## Checklist

### Before

- [x] Baseline / check / DriftResult / redacted input / advisory / empty baseline / threshold / config gap documented  
- [x] No algorithm redesign authorized  

### During (when authorized)

- [ ] Kernel + pre/post  
- [ ] Operation preserved  
- [ ] Trainer `halted_by_module_06_kernel`  
- [ ] Downstream success path stopped on contract failure  

### After

- [ ] Functional + contract + threshold boundary + Trainer halt  
- [ ] verify.sh includes M06  
- [ ] CI PASS on complete tip  
- [ ] Seal record  

---

## Test matrix (minimum)

| Case | Expected |
|------|----------|
| Topic shift / similar topic | Existing outcomes |
| Exact threshold `<` | at T → not drifted |
| Non-string | ModuleKernelError; op not run |
| Malformed / non-finite similarity / non-bool drifted | ModuleKernelError |
| Empty baseline / empty string | Preserve current semantics |
| check does not mutate baseline | Invariant |
| Trainer contract fail | halt; no PipelineResult success |
| Security block | M06 not called (existing) |
| M02/M03/M05 halt | M06 not called (existing) |

---

## Non-goals

Semantic drift · CEK · Modules 11–19 · automatic baseline learning · concurrent baseline safety claims

---

## Authorization

Implementation starts only on explicit command: **kernel Module 06**.

Until then:

```text
Decision = MIGRATE
Implementation = NOT EXECUTED
Seal = BLOCKED
```
