SWI — Structured Workflow Intelligence

Reference Implementation · Volume 1 · Part 1

SWI is a structured workflow integrity system being rebuilt from working code, automated tests, and explicitly documented limitations.

This repository contains the current reference implementation of Modules 00–10, with Module 00 acting as the pipeline orchestrator.

«Core principle:
Don't claim what hasn't been built. Don't claim what hasn't been tested. Don't hide what the implementation cannot do.»

---

What This Repository Contains

The current implementation is a single-process reference pipeline.

A message enters through Module 00 — Trainer and is processed in this order:

Input
  │
  ▼
Module 02 — Security Probe
  │
  ▼
Module 03 — Context Sync
  │
  ▼
Module 05 — Redaction Engine
  │
  ▼
Module 06 — Drift Analyzer
  │
  ├───────────────┐
  ▼               ▼
Module 07       Module 09
Memory          Audit
Validator       Logger
  │               │
  └───────┬───────┘
          ▼
       Outcome

A high security-risk score from Module 02 can halt the pipeline before downstream processing.

Every pipeline outcome is recorded through two independent hash-chain mechanisms:

- Module 07 — in-process memory validation
- Module 09 — on-disk audit logging

---

Modules

Module 00 — Trainer

The orchestrator of the reference pipeline.

It coordinates:

- Security Probe
- Context Sync
- Redaction
- Drift Analysis
- Memory Validation
- Audit Logging

Module 00 does not implement the later SWI modules and does not make autonomous decisions beyond the logic currently implemented by these modules.

---

Module 01 — Node Scanner

Checks the integrity of files or configuration at rest using SHA-256 hashes.

It can detect that content has changed.

It does not determine why the content changed and does not make the baseline itself tamper-proof.

---

Module 02 — Security Probe

Performs heuristic security checks against incoming text.

The current implementation checks for patterns associated with:

- instruction override attempts
- role override attempts
- system-prompt extraction
- zero-width characters
- base64-like payloads

It produces a bounded risk score and can trigger a pipeline halt when the configured threshold is reached.

This is a heuristic detector, not a universal injection detector.

---

Module 03 — Context Sync

Tracks timestamps and checks for:

- stale context
- out-of-order turns

The current implementation relies on the timestamp supplied by the caller.

It does not independently establish whether the supplied context is truthful.

---

Module 04 — Encryption Handler

Provides authenticated encryption using AES-256-GCM.

It supports:

- encryption
- decryption
- random nonces
- optional associated data
- tamper detection through authenticated decryption

Key management, rotation, custody, and identity infrastructure remain outside this module.

---

Module 05 — Redaction Engine

Detects and masks selected structured identifiers before downstream processing.

Current patterns include:

- email addresses
- phone numbers
- credit-card-shaped digit sequences
- Botswana Omang-shaped 9-digit identifiers

It is a first-pass structured redaction layer, not a complete PII detection system.

---

Module 06 — Drift Analyzer

Measures textual change using bag-of-words frequency vectors and cosine similarity.

It can identify significant changes against a defined baseline.

This is a coarse syntactic signal.

It is not semantic understanding and does not use embeddings.

---

Module 07 — Memory Validator

Maintains an append-only hash chain.

Each record incorporates the hash of the preceding record, allowing the chain to be checked for modification.

It can identify a broken chain and report the point of failure.

This provides tamper evidence, not tamper-proof storage.

---

Module 08 — Access Auth

Creates and validates signed, expiring session tokens using HMAC-SHA256.

The current implementation provides:

- token signing
- expiry checking
- subject identification
- constant-time signature comparison

It is not a complete identity provider and does not provide passwords, MFA, biometrics, or key custody.

---

Module 09 — Audit Logger

Writes audit records to a JSONL file using an append-only hash chain.

The chain can be independently verified to detect modification.

The current implementation does not provide remote mirroring or write-once physical storage.

---

Module 10 — External Sandbox

Executes Python code in a separate subprocess with resource controls.

The current implementation provides:

- subprocess isolation
- wall-clock timeout
- CPU limits
- memory limits
- stdout/stderr capture
- exit-status capture

It is not a hardened security sandbox against a determined adversary and does not constitute a physical network air gap.

---

What Is Actually Wired Together?

Only Module 00 directly orchestrates the reference pipeline.

Wired into Module 00

02 Security Probe
03 Context Sync
05 Redaction Engine
06 Drift Analyzer
07 Memory Validator
09 Audit Logger

Standalone utilities

01 Node Scanner
04 Encryption Handler
08 Access Auth
10 External Sandbox

These utilities can be called directly by other code but are not automatically inserted into the Module 00 pipeline.

---

Current Scope

This repository covers Modules 00–10 of the SWI architecture.

The implementation is:

- single-process
- local
- testable
- explicitly scoped
- limitation-aware

There is currently no distributed consensus layer, network propagation system, Sovereign Mesh, or multi-node enforcement mechanism implemented in this volume.

References to those concepts in earlier SWI material should not be interpreted as features of this implementation.

---

Testing

The implementation is developed against automated tests.

Run:

python3 -m pytest test_swi_core.py -v

The repository should be evaluated from the code and tests rather than from architectural claims alone.

A feature described in documentation without a corresponding runnable implementation and test should be treated as unverified.

---

Development Standard

SWI is being rebuilt using the following sequence:

Claim
  ↓
Implementation
  ↓
Test
  ↓
Result
  ↓
Limitation
  ↓
Next iteration

The documentation follows the implementation rather than the other way around.

This is intentional.

Earlier SWI material contained broader architectural claims than the accompanying implementation could demonstrate. This repository is a deliberate reset of that approach.

The objective is not to preserve every previous claim.

The objective is to determine what can actually be built, tested, measured, and demonstrated.

---

Roadmap

Future SWI modules will be added only when they have a runnable implementation and corresponding evidence.

Later architecture may include additional modules and infrastructure, but those components are not represented as implemented features until they exist in code and are tested.

---
Architectural Continuity

This repository is a verified implementation foundation, not a replacement for the broader SWI architectural work that preceded it.

Earlier SWI development explored deeper semantic, kernel-level, and higher-order architectural concepts. Those directions remain part of the broader research context of SWI, but they are intentionally not represented here as implemented capabilities unless they can be reconstructed, tested, and verified.

The purpose of this repository is to establish a reproducible foundation from which those higher-level layers can be rebuilt.

This distinction is important:

Architecture describes where SWI is intended to go.
Implementation demonstrates what SWI can currently prove.

Neither replaces the other.

As development continues, architectural concepts will be promoted into the implementation only when their definitions, mechanisms, tests, and limitations can be demonstrated in code.

---

License

License information will be added with the repository's formal release.

---

Author

Keletso Ronald Mosidila
Lead Architect & Author
Trusts Motion
Gaborone, Botswana

SWI — Structured Workflow Intelligence
