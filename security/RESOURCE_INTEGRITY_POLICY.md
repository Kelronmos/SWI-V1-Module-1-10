# SWI Resource Integrity Policy

**Document ID:** SWI-RIP-2026-10-29  
**Status:** DOCUMENTED for V1 hardening branch — NOT a universal SWI seal  
**Mission:** SWI-RI-COMPLETE-2026-10-29  
**Ceiling:** PROVEN=NO · SEALED=NO · AUTHORIZED=NO · PRODUCTION_AUTHORIZED=NO

## 1. Purpose

Define mandatory resource, path, and fail-closed controls for any SWI operation that expands, imports, unpacks, or recursively processes untrusted compressed or archive input.

```
INSPECTION ≠ ADMISSION ≠ AUTHORIZATION ≠ EXECUTION
REJECTED ≠ PROVEN
CI_GREEN ≠ SWI_AUTHORIZED
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
MATCH ≠ PERMIT ≠ EXECUTE
```

## 2. Scope

**In scope**

- ZIP inspection and extraction (`inspect_zip.py`, `extract_and_setup.py`, shared utilities)
- Future TAR or other archive formats if added
- Nested archive expansion (default: disallowed)
- Temporary extraction directories and partial output
- Setup/build paths that expand untrusted trees

**Out of scope of this document alone**

- Governing-permit redesign
- Production authorization
- Credential rotation (separate workstream)
- Claiming other repositories are secured because V1 is patched

## 3. Resource budgets (defaults)

| Limit | Default | Rationale |
|-------|---------|-----------|
| Max compressed input size | 50 MiB | Setup archives are small; prevents large uploads |
| Max per-entry expanded size | 25 MiB | Bounds single-entry bombs |
| Max cumulative expanded size | 100 MiB | Bounds multi-entry expansion |
| Max entry count | 5 000 | Bounds metadata/directory floods |
| Max nesting depth | 0 | No nested archive expansion by default |
| Max path length | 512 | Platform-safe path bound |
| Max processing time | 60 s | Wall-clock halt |
| Concurrent jobs | 1 (app-level) | Avoid concurrent exhaustion |

Untrusted input **must not** raise these limits. Operator configuration may adjust them outside the untrusted channel.

**Declared `ZipInfo.file_size` and compression ratios are not sufficient.** Limits must be enforced on actual bytes read/written during processing.

## 4. Path and filesystem rules

1. Resolve every member against a single trusted extraction root.
2. Reject absolute paths, `..` traversal, drive/UNC escapes, null bytes.
3. Do not follow symlinks or hard links outside the extraction root; prefer reject.
4. Reject unsafe special types when not explicitly supported.
5. Containment checked at write time, not only via string normalization.
6. Do not extract into sensitive application directories by default without an explicit destination argument.

## 5. Required outcomes

| Code | Meaning |
|------|---------|
| `ACCEPTED_WITHIN_POLICY` | Within limits; still ≠ authorized |
| `REJECTED_RESOURCE_LIMIT` | Size, count, nesting, or time budget exceeded |
| `REJECTED_PATH_SECURITY` | Traversal, absolute path, symlink escape |
| `REJECTED_INVALID_ARCHIVE` | Malformed, truncated, unreadable |
| `REJECTED_UNSUPPORTED_ENTRY` | Disallowed entry type |
| `INSPECTION_INCOMPLETE` | Could not finish inspection safely |
| `PROCESSING_TIMEOUT` | Deadline hit |
| `PROCESSING_FAILED` | Unexpected error; non-success |

On any non-accept outcome: stop writing, clean partial output under the destination when safe, do not report success.

## 6. Processing sequence

```
UNTRUSTED_INPUT
  → INSPECTION
  → RESOURCE_BUDGET_CHECK (running totals while reading/writing)
  → PATH_SECURITY_CHECK
  → POLICY_VALIDATION
  → [existing SWI admission/authorization if the action is executable]
  → SANDBOXED_PROCESSING (if authorized)
  → CLEANUP / EVIDENCE_RECORD
  → FINAL_STATE
```

A valid archive is not automatically admitted, authorized, or executed.

## 7. Cleanup

On reject, timeout, exception, or cancellation: close handles, remove partial trees under the designated extract root, record cleanup outcome. Never leave partial hostile content on a default downstream path.

## 8. OS-level limits

Application-level checks are necessary but not sufficient under hostile parsers. Where available, apply process memory/CPU limits, disk quotas on temp volumes, and supervisor timeouts. If OS limits cannot be applied, report the limitation; do not claim sandbox equivalence.

## 9. Evidence

Record operation id, limits, outcome code, bytes accounted (as known), whether any write occurred, cleanup result. Do not log secrets or full confidential file contents. A hash of input bytes is not a safety proof.

## 10. Status model

| State | Meaning |
|-------|---------|
| DOCUMENTED | This file |
| IMPLEMENTED | Code on a named branch |
| TESTED | Tests executed with recorded results |
| VERIFIED_WITHIN_SCOPE | Evidence supports stated properties for scoped paths |
| SEALED / AUTHORIZED / PRODUCTION_AUTHORIZED | Never granted by this policy alone |

Default for unevidenced claims: **NOT VERIFIED**.
