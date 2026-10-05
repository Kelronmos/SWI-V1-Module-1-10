# SWI V1 — Weekly Status Report

**Week:** 2026-W41 (Monday 2026-10-05 – Sunday 2026-10-11)  
**Report date:** 2026-10-05 (Monday)  
**Timezone:** Africa/Gaborone (CAT, UTC+2)  
**Live main tip SHA:** `3ea83e4d5382cc5a0e6f2e122a01ebbf31a855f2`  
**Tip date:** 2026-09-29T09:54:35Z  
**Tip message:** `docs(mutation): dual-track code+domain evidence — mutmut deferred; pilot 5/5 killed; domain 10/10`  
**Canonical inventory:** `docs/formation_path_inventory.json` (blob `6ecba6948e226f0d79dfe87550d92892fbec607e` at this tip)  
**Prior weekly:** `docs/status/WEEKLY_STATUS_2026-W40.md` (last refresh commit `3e32d27f4830dbf3aa6b819e81c7fcde87c28f25`)

> Named ≠ Implemented · Implemented ≠ Tested · Tested ≠ Sealed ≠ Authorized.
>
> This file is a status snapshot. It does **not** flip any FM status.

---

## 1. Executive snapshot

| Control | Status | Evidence basis |
|---------|--------|----------------|
| FM-001 – FM-004 | **TESTED** | Inventory `status: TESTED`; maze_protected true. Unchanged. |
| FM-005 – FM-013 | **OPEN** | Inventory `status: OPEN`; maze_protected false. **Not flipped.** |
| Universal Gate | **NOT_PROVEN** | Inventory field `universal_gate`. |
| Security Maze V1 | **NOT SEALED / NOT_READY** | Inventory `security_maze_seal`. Mutation work did not change this. |
| Foundation Seal 5 | **NOT READY** | Inventory `foundation_seal_5`. |
| External Source Admission | **IMPLEMENTED + TESTED (bounded)** · **REPLAYABLE_BOUNDED** | Prior slice; not widened this week. |
| Replay (production-wide) | **NOT_PROVEN** | Only the tested source-admission / interop contracts claim bounded replay. |
| Legal / regulatory compliance | **NOT CLAIMED** | No compliance evidence in tip lineage. |
| Production trust | **NOT CLAIMED** | Prototype / demo sink only. |

No formation-path status in `docs/formation_path_inventory.json` changed between the W40 refresh and this tip.

---

## 2. Live tip

| Field | Value |
|-------|--------|
| Branch | `main` |
| SHA | `3ea83e4d5382cc5a0e6f2e122a01ebbf31a855f2` |
| Author date | 2026-09-29T09:54:35Z |
| Week of tip commit | 2026-W40 (recorded here as the opening W41 snapshot) |
| Commits on `main` during W41 as of this report | **None** |

`docs/TIP_CI_STATUS.md` at the previous tip recorded `73a4eb1c958f191dd9c00030b47f6efb9a6e0799`. That SHA is **stale** relative to current main. Historical CI success on older SHAs is not evidence for this tip. GitHub Actions on `3ea83e4` must be verified independently; this report does not claim a green Actions run.

---

## 3. Formation geometry (inventory, unchanged)

**TESTED (do not re-read as sealed):**

- FM-001 `Trainer.process`
- FM-002 `export_foundation_evidence`
- FM-003 `sign_foundation_evidence`
- FM-004 `SecurityMaze.evaluate_request`

**OPEN (residuals preserved):**

- FM-005 `ModuleKernel.run` — default `require_admission=False`; unadmitted run forms output; not a maze authority grant. Priority-0/1 baseline added `ModuleKernel.for_privileged()` and a caller map. Default was **not** flipped to `require_admission=True`.
- FM-006 `SecurityProbe.scan` — unadmitted scan forms `ProbeResult`.
- FM-007 `ContextSync.record_turn` — unadmitted call mutates history.
- FM-008 `RedactionEngine.redact` — unadmitted call forms output.
- FM-009 `DriftAnalyzer.check` — unadmitted call forms result.
- FM-010 – FM-013 — constructor residuals; default kernel remains `require_admission=False`.

`sm_v1_014` note remains: OPEN rows require maze enforcement or explicit non-privileged reclassification before status TESTED.

---

## 4. Bounded slices (not gates)

| Control | Status | Bound |
|---------|--------|-------|
| External Source Admission | IMPLEMENTED + TESTED (bounded) | Violation → HALT; zero side-effect on tested path |
| Replay (source admission) | REPLAYABLE_BOUNDED | Same evidence hash → same decision inside tested contract only |
| CONTEXT_MISMATCH vs access-limited replay | IMPLEMENTED + TESTED (bounded) | Access limitation ≠ contextual contradiction |
| Claim slots + change control | IMPLEMENTED + TESTED (bounded) | LICENSE_IDENTIFIED ≠ LEGAL_COMPLIANCE; HASH ≠ AUTHORITY |
| External API/AI sandbox + demo journey | PROTOTYPE / TESTED | Demo sink only; declared_authority never grants AUTHORIZED |
| Interoperability 14-stage template | IMPLEMENTED + TESTED (PROTOTYPE) | QUESTION ≠ DENY; PASS ≠ authority |
| Interop mutation & replay | TESTED (10/10) on tip lineage `87163df` | Evidence under `reports/interoperability/`; not re-run for this report |
| Dual-track mutation evidence | Pilot recorded | mutmut install deferred (PyPI 502). In-repo pilot 5/5 killed; domain 10/10. Separate scores. Does **not** seal Security Maze. |
| Consequence C4/C5 auto-BLOCK | NOT fully enforced | OPEN → V3 |
| Cross-node S9 pipe | NOT_IMPLEMENTED | Separate from this V1 residual set |
| Repair baseline (`bc33232`) | Documented | Audit-reported pytest failures (execution_gate, reconstruct, route_chain) not present in this repository. Local note in that commit: 375 passed after jsonschema install. Not treated as CI evidence for `3ea83e4`. |

Bounded interop claim (only, inherited; not widened):

> Within the tested prototype scope, post-decision mutations of the tested classes do not silently reuse the original PASS.

---

## 5. Commits since last weekly status

Last weekly file update: `3e32d27f4830dbf3aa6b819e81c7fcde87c28f25` (2026-09-29, W40 refresh).

Commits on `main` after that SHA, through current tip:

| SHA | Date (UTC) | Message (subject) |
|-----|------------|-------------------|
| `bc33232c999551905cea374f952582f3e011861e` | 2026-09-29T09:43:37Z | docs(repair): baseline from tip 3e32d27 — audit scope map, observed pytest, open findings |
| `f85675e7bfff3b6fa6ef5d2055b222d89dcc3758` | 2026-09-29T09:52:20Z | docs+feat(maze): FM-005 Priority-0/1 baseline — caller map; privileged factory; no default flip |
| `3ea83e4d5382cc5a0e6f2e122a01ebbf31a855f2` | 2026-09-29T09:54:35Z | docs(mutation): dual-track code+domain evidence — mutmut deferred; pilot 5/5 killed; domain 10/10 |

None of these commits flip FM-005–013, Universal Gate, Seal 5, or compliance.

---

## 6. Explicit non-claims

| Item | Status |
|------|--------|
| Universal Gate | **NOT_PROVEN** |
| Security Maze sealed | **NOT_READY** |
| Foundation Seal 5 | **NOT READY** |
| FM-005 – FM-013 closed | **OPEN** (not flipped) |
| Production-wide replay | **NOT_PROVEN** (REPLAYABLE_BOUNDED only where tested) |
| Legal / regulatory compliance (GDPR, CCPA, AI Act, or other) | **NOT CLAIMED** |
| Production trust / authorized deployment | **NOT CLAIMED** |
| Crypto proves authority, truth, or path closure | **NOT CLAIMED** |
| mutmut score / pilot kill count as maze seal | **NOT CLAIMED** |
| Green CI on current tip | **NOT CLAIMED** (verify Actions independently) |
| V3 started | **NOT CLAIMED** (V3 start freeze record only, earlier lineage) |

---

## 7. Recommended next priorities

Honest order: **Specify → Implement → Test → Replay → Prove**. Do not skip a step to claim the next.

1. **Specify** FM-005–013 closure conditions: which call sites must use `ModuleKernel.for_privileged()`, which remain compatibility, and what evidence would justify reclassification. Do not specify a global `require_admission=True` default without a caller-breakage inventory (already noted as breaking modules without admission APIs).
2. **Implement** only the specified privileged paths. Leave inventory status OPEN until enforcement matches the specified residual.
3. **Test** each residual with adversarial cases that fail closed (unadmitted formation must not look like maze authority). Record observed pytest; do not treat a local count as CI.
4. **Replay** only inside the contract under test. Keep REPLAYABLE_BOUNDED. Do not promote to production-wide replay.
5. **Prove** Universal Gate only after OPEN rows are enforced or explicitly reclassified, and after an independent tip CI run. Until then: **NOT_PROVEN**. Seal 5 stays **NOT READY**. Compliance stays **NOT CLAIMED**.

Secondary, still not a status flip: re-check GitHub Actions on `3ea83e4`; finish or explicitly defer mutmut (install was unavailable); keep C4/C5 and S9 as V3 items, not V1 seal evidence.

---

**End of weekly status 2026-W41.** No FM flips.
