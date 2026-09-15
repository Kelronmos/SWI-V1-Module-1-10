# SWI Cross-Repository Trust Specification

**Status:** **PROPOSED / DESIGN PENDING**  
**Author:** Keletso Ronald Mosidila — Trusts Motion · 15 September 2026

## Correct hierarchy (not “CA cert = task”)

```text
Trusted CA
  → Repository / Service Certificate
      → Public Key
Private Signing Key  →  Task Signature
  → Signed Task Envelope
  → CRTG (PROPOSED)
  → M11 → AdmittedInput → V2 Kernel → M12+
```

**Canonical requirement:**  
Each cross-repository task MUST carry a **verifiable signer identity** and a **signature under an active key** recognized by the current trust policy.

The certificate identifies the signer. The private key signs the task.  
The certificate itself does not “be” the task signature.

## Distinctions

Certificate validity ≠ task validity ≠ evidence truth ≠ safe action.

## Not implemented

CRTG · CA issuance · trust store · envelope · rotation · revocation · replay · CI.

Private keys must never appear in Git.

See also: `docs/CROSS_REPOSITORY_TRUST_INTEGRATION.md` · V2 copy of this design posture.
