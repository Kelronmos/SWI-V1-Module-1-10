# SWI Mutation Evidence — Dual Track

**Rule:** Code mutation and domain mutation are **independent** evidence tracks. Do not merge into one score.

```
CODE MUTATION  →  Do tests detect bad code?     →  TEST EVIDENCE
DOMAIN MUTATION →  Do decisions react to facts? →  GOVERNANCE EVIDENCE
```

Neither track seals Security Maze or proves Universal Gate.

## Layout

```
reports/mutation/
  README.md
  baseline.json
  code/
  domain/
  <sha>/
```

## Tools

| Track | Preferred tool | This pilot |
|-------|----------------|------------|
| Code | mutmut / Cosmic Ray | **In-repo pilot** (mutmut install failed: PyPI 502) |
| Domain | M01–M10 adversarial suite | **Executed** |

## Non-claims

- Mutation score ≠ Security Maze SEALED
- Mutation score ≠ Universal Gate PROVEN
- Mutation score ≠ production trust
