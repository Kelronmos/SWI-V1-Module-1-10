# Evidence Matrix

| Claim | Evidence | Status |
|-------|----------|--------|
| M02/M03/M05 kernel + halt | Code + tests + prior CI | **SEALED** |
| M06 kernel + config + halt | Code + tests + CI run 34968919030 on `8a44c52` | **SEALED** |
| M07/M09 Trainer integrity | Code + `test_trainer_persistence_integrity.py` | TESTED · not sealed |
| Foundation Seal 5 | Checklist incomplete | **NOT READY** |
| CRTG / certificates | Spec only | **PROPOSED** |
| V1 evidence export for V2 | — | **NOT IMPLEMENTED** |
| Modules 11–46 in V1 | — | **BLOCKED** |
| Proposed Module 10 BoundaryExporter (M07→M08→M09→M10 chain) | Red-team review 2026-09-19; no integration with canonical path | **PROPOSED / NOT ADMITTED** |
| Existing Module 10 External Sandbox | Code + tests (subprocess isolation) | IMPLEMENTED / LIMITED (see KNOWN_LIMITATIONS) |

Latest tip CI: re-check Actions for the exact SHA before sealing any new change. An older green run does not seal a newer commit.

**Rule:** Module number is not permission. Proposed components remain construction references until the full evidence chain is satisfied.
