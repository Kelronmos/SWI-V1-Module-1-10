# Evidence Matrix

**SEALED** means: documented contract + tests + failure propagation + independent CI on a known commit.  
It does **not** mean complete security, semantic understanding, or universal safety.

| Claim | Evidence | Status |
|-------|----------|--------|
| Trainer multi-module pipeline | `module00_trainer.py` + tests | tested |
| Config YAML / thresholds applied | `config_loader` + Trainer tests | tested |
| **M02** kernel I/O contract | `module02_security_probe.py` + `test_security_probe_kernel.py` | **SEALED** — enforcement |
| **M02** adversarial boundaries | `test/adversarial/test_security_probe_boundaries.py` | **SEALED** — limits documented |
| **M02** Trainer halt / no silent continue | `test/test_trainer_kernel_halt.py` | **SEALED** |
| **M02** config `block_threshold` | config_loader + Trainer tests | **SEALED** |
| **M02** detection complete / non-bypassable | — | **not claimed** |
| **M02** seal record | `docs/MODULE_02_SEAL_RECORD.md` | **SEALED** |
| Contract fail → HALT vs risk → `allowed=False` | Trainer + M02 docs | documented |
| **M03** kernel + Trainer halt | seal record + CI #26 | **SEALED** |
| **M05** kernel + structured-PII only | seal/evidence docs + tests | **SEALED** |
| **M06** kernel | — | INSPECTED · MIGRATE · **not executed** |
| Hardened sandbox | — | **not claimed** |
| CEK / Vector Memory / Alita | — | **not claimed** |
| Modules 11–19 | — | **blocked until Seal 5** |
| CI independent witness | Actions (e.g. [#26](https://github.com/Kelronmos/SWI-V1-Module-1-10/actions/runs/34789422861), [#29](https://github.com/Kelronmos/SWI-V1-Module-1-10/actions/runs/34790281579)) | **PASS** on cited runs — not “verify in UI” alone |
