# SWI V4.7 Module Map (Construction Reference)

**Status:** MAPPED  
**Authority:** Construction reference only — not a completion claim.

This map indicates where future work may belong. Presence of a number does not mean the module is implemented, tested, or sealed.

## Formal / Verification

| ID | Concern | Location |
|----|---------|----------|
| W1–W3 | Admission-gated workflow safety | `verification/tla/v47/` |
| FM-005 | Ungated formation residual | OPEN — negative-control model only |
| S9 | Reachability / SCC / termination | Separate track |

## Core pipeline (historical V1)

| Module | Role | Status note |
|--------|------|-------------|
| M02 | Security probe | SEALED (historical) |
| M03 | Context sync | SEALED (historical) |
| M05 | Redaction | SEALED (historical) |
| M06 | Drift | Kernel-enforced |
| M11 | Continuity | Implemented / tested |

Do not promote status merely because this map exists.
