# SWI V3 — Roadmap Note (not this repository)

V3 is a **separate** prototype/research repository. Do not mix runtime/consequence completion into sealed V1 history without evidence.

**Suggested name:** `Kelronmos/SWI-V3-Prototype` (create manually; this connector cannot create repositories).

## Module sketch (SPECIFIED only until implemented elsewhere)

| Module | Purpose |
|--------|---------|
| M23 Secure Pipe | Controlled movement; quarantine, provenance, integrity |
| M24 Information Sharing | S9/evidence share without transferring authority |
| M25 Authority Boundary | Claims ≠ established authority |
| M26 Runtime Binding | Bind decision + evidence + context to a runtime |
| M27 Consequence Gate | C0–C5; C4/C5 not executable in prototype |
| M28 Advisory Engine | Recommend/review without executing |
| M29 Safe Runtime | Simulation-only sink |
| M30 Halt Enforcement | HALT/BLOCK → protected ops = 0 calls |
| M31 Replay & S9 | Tamper / decision comparison |
| M32 Evidence Vault | Manifests, hashes, recovery metadata |
| M33 Backup-of-Backup | Independent recovery index |
| M34 SWI Discipline | UNKNOWN ≠ FALSE, etc. |
| M35 Adversarial Maze | Attack pipe/authority/runtime/consequence |
| M36 Prototype Verification | JSON/Markdown evidence package |

## Central invariants (for V3 README when created)

```
PIPE ≠ TRUST
HASH ≠ AUTHORITY
EVIDENCE ≠ AUTHORITY ≠ DECISION ≠ EXECUTION
RUNTIME ≠ PERMISSION
ADVISORY ≠ EXECUTION
SIMULATION ≠ REAL-WORLD EFFECT
PASS ≠ UNIVERSAL AUTHORITY
UNKNOWN ≠ FALSE
HALT MUST CONTAIN THE CONSEQUENCE
```

S9: Node B may verify an evidence package; it must **not** inherit Node A's authority automatically.

**Status of this note:** DOCUMENTATION ONLY · V3 repository: NOT CREATED BY THIS WRITE · Production: NOT CLAIMED
