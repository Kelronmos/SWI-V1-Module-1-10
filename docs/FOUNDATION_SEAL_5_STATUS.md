# Foundation Seal 5 — Path Status

**Date:** 2026-09-17  
**Status:** **PATH OPEN / NOT SEALED**

## What exists

| Item | State |
|------|--------|
| Integrity digest on export | Existing |
| Optional Ed25519 over integrity-bound material | **Implemented** (`sign_foundation_evidence` / `verify_signed_foundation_evidence`) |
| Unit tests | `test/test_foundation_seal5.py` |
| Private keys in git | **Forbidden** |
| Pinned production public key | **Empty** (`SEAL5_PINNED_PUBLIC_KEY_HEX`) |
| CI job verifies signature every run | **Not yet** |
| CRTG / HSM / rotation | **Not implemented** |

## Sign material

`evidence_id`, `foundation_version`, `evidence_schema_version`, `integrity_reference`, `source_reference`, `verification_status`, `seal5_version`.

`created_at` is not signed.

## Non-claims

Signature ≠ factual truth · ≠ production custody · ≠ Seal 5 complete until pin + CI verify + audit.

## Next

1. CI: sign export (secret/ephemeral) · verify · publish public key as artifact  
2. Pin verification public key when operational model exists  
3. Independent verifier checks Seal 5 when present  
