# Private Canonical / Public Mirror Security Model

**Status:** TARGET MODEL — partially provisioned  
**Date:** 2026-09-19  
**Public repository (this tree):** `Kelronmos/SWI-V1-Module-1-10` (currently **public**)  
**Private canonical repository:** `Kelronmos/SWI-V1-Canonical` (created **private**)

---

## Target structure

```text
PRIVATE CANONICAL REPOSITORY (SWI-V1-Canonical)
        │
        ├── sensitive SWI kernel
        ├── admission boundary
        ├── governance / authorization
        ├── cryptographic evidence paths
        ├── security / adversarial tests
        ├── developer-only construction modules
        └── protected CI/CD
                 │
                 ▼
        SANITIZED PUBLIC SURFACE (optional)
        │
        ├── documentation
        ├── reproducible examples
        ├── non-sensitive tests
        └── no secrets / no internal control planes as sole authority
```

Private access reduces exposure. It is **not** a substitute for secret management, branch protection, or CODEOWNERS.

---

## What has been done

| Step | Status |
|------|--------|
| Create private empty canonical repo `SWI-V1-Canonical` | **DONE** |
| Document security model | **DONE** (this file) |
| CODEOWNERS for sensitive paths | **DONE** (this repo) |
| Import full history into private canonical | **NOT DONE** — requires local/admin git migration |
| Branch protection / rulesets on main | **ATTEMPT SEPARATELY** — verify in Settings |
| Make public repo private or delete | **NOT DONE** — forbidden until private import verified |
| Sanitized public mirror of non-sensitive docs only | **NOT DONE** |

---

## Safe migration sequence (do not skip)

1. Freeze feature work on public tip; record tip SHA.  
2. Confirm `SWI-V1-Canonical` is **private**.  
3. Locally: clone public history → push to private canonical (preserve commits).  
4. Verify commit SHAs and tree on private remote.  
5. Protect `main` on private: no direct push, no force push, no delete, required PR, required CI, CODEOWNERS.  
6. Restrict collaborators to least privilege.  
7. Run full adversarial + `./scripts/verify.sh` on private tip.  
8. Only then: archive or delete public copy **or** replace public with a sanitised subset.  
9. Never put real credentials in either repository.

**Do not delete the public repository until steps 3–7 are verified.**

---

## Sensitive paths (CODEOWNERS + review required)

- `swi_core/admission_boundary.py`
- `swi_core/`
- `security/`
- `test/adversarial/`, `test/`, `tests/`
- `.github/workflows/`
- `scripts/verify.sh`, claim-language scripts
- governance / evidence matrix / admission status docs

---

## Branch protection targets (apply in GitHub Settings or rulesets)

```text
direct push to main       = DENY
force push                = DENY
deletion of main          = DENY
required pull request     = YES
required status checks    = YES (CI)
CODEOWNERS approval       = YES
sensitive-path approval   = YES
```

---

## Distinction

| Control | Role |
|---------|------|
| Private repository | Reduces casual exposure |
| Branch protection | Prevents unilateral main changes |
| CODEOWNERS | Forces review on sensitive paths |
| Admission boundary tests | Executable anti-overclaim |
| Secret management (outside git) | Credentials never in source |

Making a repo private alone does **not** implement the other rows.

---

## Non-claims

- This document does not change visibility of `SWI-V1-Module-1-10`.
- Creating `SWI-V1-Canonical` does not import history by itself.
- CODEOWNERS without required-review rulesets is advisory only.
- No claim that secrets were scanned or absent.

**Do not claim what the code and account settings cannot demonstrate.**
