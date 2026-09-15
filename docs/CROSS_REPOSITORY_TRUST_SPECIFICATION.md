# SWI Cross-Repository Certificate, Identity & Key-Rotation Trust Manual

**Version:** 1.0 — Design Specification  
**Date:** 15 September 2026  
**Author:** Keletso Ronald Mosidila — Trusts Motion  
**Status:** **PROPOSED / DESIGN PENDING**

> This document is a **specification**. It is **not** implementation evidence.  
> No CA, CRTG, signing, rotation, or replay protection is claimed as implemented until code + tests + CI exist.

## 1. Purpose

Define the trust boundary so a cross-repository task cannot enter an SWI-controlled pipeline merely because the repo is known, the payload parses, a certificate *exists*, or the sender *claims* trust.

Required before admission:

1. Recognized sender identity  
2. Valid certificate (chain to trusted CA, purpose, validity)  
3. Signing key recognized and permitted by rotation policy  
4. Task actually signed by that key  
5. Integrity of signed material  
6. Expiry / replay policy  
7. Admission contract (e.g. M11)

## 2. Core principle

```text
No cross-repository task crosses the SWI trust boundary until
signer identity, certificate chain, key state, signature,
and task envelope have been verified.
```

Proposed sequence:

```text
External Repo → Task → Signing Key → Signature + Certificate
        → CRTG (PROPOSED) → M11 → AdmittedInput → V2 Kernel → M12–22
```

## 3. Distinctions (mandatory)

| Concept | Does **not** prove |
|---------|---------------------|
| Valid certificate | Truth of payload |
| Valid signature | Safety of action |
| Admission | Universal correctness |
| Successful execution | Underlying assumption true |

**Certificate = identity under a hierarchy**  
**Signature = authenticity/integrity of signed bytes**  
Neither is truth verification.

## 4. Status matrix

| Component | Status |
|-----------|--------|
| CRTG | **PROPOSED** |
| CA hierarchy | DESIGN PENDING |
| Certificate profile | DESIGN PENDING |
| Trust store | DESIGN PENDING |
| Task envelope | DESIGN PENDING |
| Task signing / verification | DESIGN PENDING |
| Key rotation / revocation | DESIGN PENDING |
| Replay protection | DESIGN PENDING |
| CI / production | NOT IMPLEMENTED |

## 5. Trust hierarchy (proposed)

```text
ROOT / TRUSTED CA
  └── Repository / Service CA
        └── Repository Certificate
              └── Signing Key → Signed Task
```

Identities (examples): V1 repo, V2 repo, Firefly adapter, Rust adapter, Evidence Engine.  
**Do not** trust arbitrary syntactically valid certificates.

## 6. Private key rule

Private keys **MUST NOT** appear in Git, source, README, fixtures, public logs, or task payloads.  
Dev/test keys separated from production.

## 7. Task envelope (conceptual — freeze before code)

Fields: `task_id`, `task_type`, `schema_version`, source repo/pipeline/env, `certificate_serial`, `key_id` / `key_version`, `created_at` / `expires_at`, nonce, `payload` / `payload_hash`, `signature`.

Canonical serialization **must** be specified before implementation (no ambiguous JSON field order).

## 8. CRTG responsibilities vs non-responsibilities

**Does:** chain, CA, dates, purpose, identity, key state, signature, payload hash, schema, expiry, replay (if implemented), trust-policy version.

**Does not:** decide truth, ethics, or final safety of action (downstream).

## 9. Fail-closed

Missing/invalid cert, untrusted CA, expired cert, wrong purpose, unknown repo/key, retired/revoked key, bad signature, payload change, expired task, unsupported schema → **REJECT / HALT** (exact labels frozen at implement time).

## 10. Key lifecycle (proposed)

`ACTIVE` → `ROTATING` → `RETIRED` · compromise → `REVOKED`  
Overlap windows explicit in trust policy. Retired keys not silently permanent.

## 11. Replay

Valid signature alone does **not** prevent replay. Claim replay protection only after a chosen mechanism exists and is tested.

## 12. Crypto rule

Use established standards only (e.g. proposed X.509 + Ed25519 + SHA-256 — still **PROPOSED**).  
No custom crypto algorithms.

## 13. Ordering with V1/V2

```text
V1 foundation evidence → CRTG → M11 → AdmittedInput → Kernel → M12+
```

Unauthenticated material must not become `AdmittedInput`.  
CRTG success does not bypass M11.

## 14. Implementation gate (do not reverse)

Freeze profile → envelope → canonical bytes → key lifecycle → rotation/revocation/replay → CRTG contract → implement → negative tests → positive tests → CI → clean clone → claim audit → seal.

## 15. What this does **not** claim

Universal security · truth of evidence · perfect compromise detection · tamper-proof storage · production readiness of CRTG.

## 16. Canonical statement

> Every cross-repository task MUST arrive with a verifiable signer identity and a signature under a key recognized by the current trust policy. A valid certificate establishes identity; a valid signature establishes integrity of signed material. Neither establishes truth of claims nor safety of action.
