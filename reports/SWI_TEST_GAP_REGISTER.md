# SWI Test Gap Register (2026-10-29, updated)

| Issue | Investigation | Reproduction | Fix | Regression test | Review |
|-------|---------------|--------------|-----|-----------------|--------|
| V2 empty-capability | CONFIRMED (vacuous ∅ ⊆ X → PERMITTED on de374da7) | YES (local) | YES on branch `security/empty-capability-never-permit-2026-10-29` tip `ac8c5f81…` | YES (21 passed local) | PENDING; **not merged to main** |
| Firefly OTP→replay_permission | CONFIRMED_IN_SOURCE | Inspection only | PARTIAL (SMTP env) | NOT_RUN | PENDING |
| V4 build_engine.py | ABSENT at 2e8ced1e | N/A | NOT_IMPLEMENTED | BLOCKED | PENDING |
| Independent human review | PENDING | — | — | — | PENDING |
| Cross-repo E2E | NOT_IMPLEMENTED | — | — | — | PENDING |
| Packaging 16-case tool suite | PARTIAL | — | — | NOT fully completed | PENDING |

## Independent package digests (recalculated 2026-10-29)

| Artifact | Expected | Recalculated | Match |
|----------|----------|--------------|-------|
| ZIP `SWI-Evidence-Package-2026-10-29-v1.zip` | c74a2348ae3547a7ae4b19889a20d3b7946c9e8319cd74e54415a84fc6a61dca | same | YES |
| Manifest `CLAIM_TEST_REPLAY_MANIFEST.json` | d119968b23ecfdfef4ac3fb035d9f56461acad9286e223a86d213303898c815a | same | YES |

ZIP: 26116 bytes, 32 entries, testzip OK, no unsafe paths.

PROVEN=NO SEALED=NO AUTHORIZED=NO PRODUCTION_AUTHORIZED=NO
