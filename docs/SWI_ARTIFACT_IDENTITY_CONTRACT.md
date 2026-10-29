# SWI Artifact Identity Contract

**Schema:** `swi.artifact-identity.v1`  
**Mission:** SWI-TRACE-PROOF-2026-10-29  
**Status:** REFERENCE CONTRACT — not universal seal  

```
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
MATCH ≠ PERMIT ≠ EXECUTE
Hash verification ≠ authorization
Serial ≠ authenticity proof
Timestamp ≠ trusted time (unless independently verified)

PROVEN = NO (default)
SEALED = NO (default)
AUTHORIZED = NO (default)
PRODUCTION_AUTHORIZED = NO (default)
```

## 1. Purpose

Assign stable identity and content integrity metadata to SWI artifacts without promoting them to proof or authorization.

## 2. Core distinctions

| Concept | Meaning |
|---------|---------|
| `artifact_id` | Stable unique ID for one artifact version |
| `serial` | Human-readable label; not an auth token |
| `content.digest` | SHA-256 of exact stored bytes |
| `task_id` / `execution_id` | Separate from artifact identity |
| `integrity_status` | Result of digest recalculation |
| `proof_status` | Separate SWI proof procedure |
| `authorization_status` | Separate governing decision |

Changing content **must** yield a new digest and a new artifact version record. Never silently replace a historical digest.

## 3. Required fields (v1)

See `schemas/swi_artifact_identity_v1.json`.

Minimum:

- `schema`, `artifact_id`, `serial`, `artifact_type`
- `created_at` (RFC3339), `timestamp_source`, `timestamp_trust`
- `origin_type`
- `content.media_type`, `content.size_bytes`, `content.hash_algorithm`, `content.digest`
- `integrity_status`, `signature_status`, `proof_status`, `authorization_status`, `replay_status`
- `record_version`

## 4. Serial format (reference)

```
SWI-ART-YYYYMMDD-<12 hex chars>
SWI-TASK-YYYYMMDD-<12 hex chars>
SWI-IMP-YYYYMMDD-<12 hex chars>
SWI-EXP-YYYYMMDD-<12 hex chars>
SWI-RPL-YYYYMMDD-<12 hex chars>
```

Suffix from `secrets.token_hex(6)` (or equivalent CSPRNG). Timestamp alone is insufficient. Serials are not authorization tokens. External imported IDs are preserved separately and not overwritten.

## 5. Hashing rules

- Algorithm: `SHA-256`
- Digest encoding: lowercase hex
- Files/archives: hash exact stored bytes (streaming for large files)
- Structured data: define canonical JSON (sorted keys, UTF-8, no insignificant whitespace) before `CANONICAL_DATA_HASH`
- Distinguish `RAW_CONTENT_HASH` vs `CANONICAL_DATA_HASH` vs `MANIFEST_HASH` vs `SIGNATURE`

Client-supplied digests must be recomputed before acceptance as verified.

## 6. Timestamp trust

| Value | Meaning |
|-------|---------|
| `UNVERIFIED` | Local system clock or unknown |
| `UNKNOWN` | Legacy / missing |
| `EXTERNAL_TSA` | Only if independent TSA used (optional) |

Never invent timestamps for unrecorded events. Never backdate migration time as original creation.

## 7. Status fields (no automatic promotion)

- `integrity_status`: `UNVERIFIED` | `MATCH` | `MISMATCH` | `UNAVAILABLE`
- `signature_status`: `UNSIGNED` | `VALID` | `INVALID` | `UNKNOWN_KEY`
- `proof_status`: `NOT_PROVEN` | `PROOF_PENDING` | `PROOF_PASSED_WITHIN_SCOPE` | `PROOF_FAILED` | `PROOF_INCOMPLETE`
- `authorization_status`: `NOT_AUTHORIZED` | (other values only from real SWI authority path)
- `replay_status`: `NOT_REPLAYED` | `REPLAY_MATCH` | `REPLAY_MISMATCH` | `REPLAY_FAILED` | `REPLAY_INCOMPLETE`

Passing integrity **must not** set proof or authorization to success.

## 8. Events (illustrative vocabulary)

Emit only events that occurred. Example types: `ARTIFACT_CREATED`, `ARTIFACT_HASHED`, `ARTIFACT_REGISTERED`, `ARTIFACT_VERIFIED`, `IMPORT_COMPLETED`, `DOWNLOAD_RECORDED`, `REPRINT_RECORDED`, `REPLAY_*`, `REJECTED_*`.

## 9. Interoperability

Cross-language adapters must share:

- Schema version id
- SHA-256 test vectors
- Canonical JSON rules for structured hashes
- Serial prefix conventions

Do not claim cross-repo conformance until shared tests pass in each language.

## 10. Security

No secrets in manifests. No path traversal via artifact IDs. No unauthenticated private retrieval by serial alone. Apply resource integrity policy to imports/archives.
