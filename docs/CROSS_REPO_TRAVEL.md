# Cross-Repository Travel Boundary

## Status

| Gate | State |
|------|--------|
| Local export → JSON | **PROVEN** |
| Real producer script | `scripts/export_travel_evidence.py` |
| V2 M11 seal | **NOT SEALED** (see V2 `docs/M11_FINAL_AUDIT_REPORT.md`) |
| Two-checkout CI_VERIFIED | V2 responsibility · tip-specific |

## Path

```text
Trainer → export_foundation_evidence → JSON → V2 M11
```

M10 is not the handoff. V2 must not import this package.

Integrity: five covered fields; **created_at excluded**.
