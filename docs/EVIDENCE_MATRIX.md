# Evidence Matrix

**SEALED** = documented contract + tests + failure propagation + independent CI on a known commit.  
Not complete security, semantic understanding, or universal safety.

| Claim | Evidence | Status |
|-------|----------|--------|
| Trainer multi-module pipeline | `module00_trainer.py` + tests | tested |
| Config block/staleness/drift thresholds | `config_loader` + Trainer tests | tested |
| M02 kernel + halt | seal record + tests | **SEALED** |
| M03 kernel + halt | seal record + tests | **SEALED** |
| M05 kernel + structured PII only | seal/evidence + tests | **SEALED** |
| M06 kernel (lexical/cosine) | `module06_*` + `test_drift_kernel.py` | **KERNEL-ENFORCED** · local PASS · **CI SEAL PENDING** |
| M07 Trainer integrity/persistence | `test_trainer_persistence_integrity.py` | tested · not kernel-sealed |
| M09 Trainer integrity/persistence | same | tested · not kernel-sealed |
| Foundation Seal 5 | — | **NOT READY** |
| Modules 11–20 in V1 | — | **BLOCKED** |
| CEK / Vector Memory / Alita | — | **not claimed** |
