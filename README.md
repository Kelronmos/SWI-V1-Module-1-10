Structured Workflow Intelligence (SWI)

Modules 00–10 — Verified Reference Implementation

Author: Keletso Ronald Mosidila
Organisation: Trusts Motion
Status: Active Reconstruction / Verified Reference Implementation

---

What This Repository Is

This repository contains the currently reproducible implementation of the SWI Modules 00–10 reference implementation.

It establishes a local, single-process engineering foundation for mechanisms that can currently be inspected in source code, exercised through automated tests, and described from observed behaviour.

This repository is not a complete reconstruction of the broader SWI architecture or of every capability, prototype, research direction, or architectural concept previously explored under SWI.

«What is implemented must be distinguishable from what is remembered, proposed, or intended.»

---

Verification Boundary

The current repository should be evaluated from its code, tests, and documented behaviour rather than from architectural claims alone.

Status| Meaning
Implemented| Functionality exists in the repository and can be inspected in source code.
Tested| Functionality is supported by executable automated tests.
Architectural| A design or mechanism is defined as a direction but is not sufficiently implemented and verified here.
Historical| A capability or prototype may have existed in earlier development but cannot currently be reconstructed from surviving evidence.

These categories are deliberately kept separate.

The rebuild therefore prioritises reproducibility over reconstruction by memory.

«Remembering that something existed is not the same as being able to prove that it exists.»

---

Current Scope

The current repository provides a verified implementation foundation for Modules 00–10.

It is a local, single-process implementation. Module 00 — Trainer is the primary orchestrator for the modules currently wired into its execution path.

Integrated Pipeline

Input
  │
  ▼
Module 00 — Trainer
  │
  ├── Module 02 — Security Probe
  ├── Module 03 — Context Sync
  ├── Module 05 — Redaction
  ├── Module 06 — Drift Detection
  ├── Module 07 — Memory Validator
  └── Module 09 — Audit Logger

Module 03 — Context Sync is part of the Trainer execution flow. However, the current "Trainer.process()" interface does not accept an explicit timestamp. Therefore, its timestamp-based staleness and out-of-order validation are currently exercised through direct "ContextSync" usage rather than through the default Trainer pipeline.

This distinction is intentional: a module being wired into a pipeline does not mean every capability of that module is exercised by every integration path.

Standalone Components

The following modules are implemented in the repository but are not directly invoked by Module 00's default execution path:

- Module 01 — SHA-256 Node Scanner
- Module 04 — AES-256-GCM Encryption
- Module 08 — Access Authentication / Tokens
- Module 10 — External Sandbox

A module existing in the repository does not automatically mean that it is part of the default execution path.

---

Module Overview

Module| Component| Current Role| Default Trainer Path
00| Trainer| Pipeline orchestration| Yes
01| Node Scanner| SHA-256 integrity scanning| No
02| Security Probe| Heuristic instruction/injection risk detection| Yes
03| Context Sync| Turn ordering and timestamp-based context validation| Yes, with timestamp limitation
04| Encryption| AES-256-GCM encryption utility| No
05| Redaction| Sensitive-content handling| Yes
06| Drift Detection| Coarse context/drift analysis| Yes
07| Memory Validator| Hash-chain memory consistency validation| Yes
08| Access Auth| Authentication/token handling| No
09| Audit Logger| Audit/event recording| Yes
10| External Sandbox| Resource-controlled external execution boundary| No

---

Implementation Boundaries

This repository is a reference implementation of specific workflow, integrity, security, validation, and audit mechanisms.

It should not be represented as a complete autonomous AI governance system.

Module 02 — Security Probe

The security probe uses bounded heuristic checks for patterns associated with instruction or role override, system-prompt extraction, zero-width characters, and other suspicious input patterns.

It is not a universal prompt-injection detector and does not establish that all malicious input will be detected.

Module 03 — Context Sync

Module 03 supports explicit timestamp-based context validation, including stale and out-of-order checks, when used directly.

The current "Trainer.process()" interface does not expose a timestamp parameter. The default Trainer pipeline therefore cannot currently supply conversation timestamps to Module 03 for those checks.

This is an implementation boundary, not a claim that the underlying Module 03 capability does not exist.

Future work may wire timestamp input through Module 00 once the interface and corresponding tests are defined and verified.

Module 04 — Encryption

Module 04 provides AES-256-GCM encryption/decryption with authenticated integrity checks. Key management and secure key custody are outside the scope of this reference implementation.

Module 05 — Redaction

Module 05 performs structured first-pass redaction for supported sensitive patterns. It is not a complete PII discovery or classification system.

Module 06 — Drift Detection

The current drift mechanism uses a coarse syntactic approach based on token/frequency similarity.

It should not be described as semantic understanding, consciousness, reasoning about meaning, or proof that a system understands context.

Module 07 — Memory Validation

The memory validator uses an append-only hash-chain mechanism to expose alteration of the recorded chain. It is tamper-evident, not tamper-proof.

Module 08 — Access Authentication

Module 08 provides signed, expiring token handling within the reference implementation. It is not a complete identity provider and does not provide a full password, MFA, biometric, or enterprise key-custody system.

Module 09 — Audit Logger

Module 09 records audit events using a hash-linked append-only JSONL structure. It does not by itself provide remote mirroring, immutable physical storage, or complete operational audit infrastructure.

Module 10 — External Sandbox

Module 10 provides a resource-controlled Python subprocess boundary. It should not be represented as a hardened security sandbox, container isolation system, or physical network air gap.

Security

The presence of security, authentication, encryption, audit, or validation mechanisms does not by itself establish complete system security.

Each mechanism has a defined scope, assumptions, and limitations.

Distributed Architecture

The following are not implemented in this volume:

- distributed consensus;
- network propagation;
- Sovereign Mesh;
- multi-node enforcement; and
- other distributed execution mechanisms.

References to these concepts in earlier SWI material are architectural or historical context, not evidence of functionality contained in this repository.

---

Configuration Boundary

"config/swi_config.yaml" currently documents intended module settings such as thresholds and key lengths, but the current "swi_core" implementation does not load this YAML file at runtime.

Runtime settings are supplied through module constructors or code-level parameters.

Therefore, editing "config/swi_config.yaml" does not currently change runtime behaviour. It should be treated as a configuration/design reference until a verified configuration loader is implemented.

---

Testing

Tests demonstrate the behaviour covered by the current implementation. They are not evidence of capabilities outside their coverage.

The current repository documentation identifies 22 automated tests in "test_swi_core.py".

The documented coverage includes areas such as:

- node integrity and tamper detection;
- instruction-override/injection detection;
- direct context ordering and staleness validation;
- redaction behaviour;
- drift handling;
- memory validation; and
- audit logging.

Run the test suite from the repository root:

python3 -m pytest test_swi_core.py -v

For the Makefile test target:

make test

For coverage:

make coverage

A passing test demonstrates the behaviour exercised by that test under the conditions in which it ran. It does not establish that the entire SWI architecture, or any capability outside the test's coverage, has been proven.

---

Evidence and Verification

The implementation should be evaluated through this chain:

Claim
  ↓
Implementation
  ↓
Test
  ↓
Observed Result
  ↓
Documented Limitation
  ↓
Next Iteration

The rule is simple:

«Claim only what the current evidence can support.»

This is the central discipline of the reconstruction.

---

Integrity Terminology

This project deliberately uses tamper-evident rather than tamper-proof terminology.

A tamper-evident mechanism is intended to detect or expose alteration. It does not imply that alteration is impossible.

Likewise, tested means that the relevant automated tests pass under the conditions covered by those tests. It does not mean that the entire system is universally proven secure, correct, or complete.

---

Architectural Continuity

SWI has developed through research, experimentation, architectural discussion, and implementation across multiple stages.

Earlier work explored deeper semantic, kernel-level, and higher-order architectural concepts. Those directions remain part of the broader SWI research context.

They are not presented here as implemented capabilities unless they can be reconstructed, implemented, tested, and verified.

This repository is therefore not a replacement for the broader SWI architecture. It is the verified implementation layer being rebuilt from surviving, reproducible evidence.

«Architecture describes where SWI is intended to go.
Implementation demonstrates what SWI can currently prove.»

The absence of a concept from this repository does not mean that the concept was abandoned. Likewise, mentioning an architectural concept does not mean that it has been implemented.

---

Reconstruction Principle

Earlier SWI development grew beyond what is currently preserved in this repository.

Some capabilities can still be remembered or described, while the surviving code may not be sufficient to reproduce or prove them.

The rebuild therefore does not recreate missing functionality simply because it is remembered.

Instead:

1. surviving code is inspected;
2. behaviour is reproduced;
3. tests are written or executed;
4. limitations are documented;
5. architectural concepts remain clearly labelled; and
6. new implementation is added only when it can be verified.

«Reconstruction must follow evidence, not memory.»

This protects the project from turning historical recollection into unsupported technical claims.

---

Future Development

The current implementation does not define the final boundary of SWI.

Future work may include deeper semantic and kernel-level mechanisms, broader workflow intelligence, distributed components, multi-node enforcement, and other architectural layers.

Those capabilities should be added only when their implementation and verification support the claims made about them.

The intended progression is:

Architectural Research
        │
        ▼
Defined Mechanism
        │
        ▼
Implementation
        │
        ▼
Testing
        │
        ▼
Verification
        │
        ▼
Broader SWI Architecture

This allows the broader architecture to evolve without confusing architectural intent with implemented capability.

---

Development Status

Active Reconstruction

Current priorities are:

1. establish a reproducible foundation;
2. verify each implementation;
3. document actual behaviour;
4. identify limitations;
5. separate implementation from architectural intent;
6. reconstruct higher-level components progressively; and
7. avoid unsupported claims.

The objective is not to make SWI appear larger.

The objective is to make the implementation accurate, reproducible, inspectable, and challengeable.

---

Intellectual Context and Attribution

SWI has developed through research, experimentation, architectural challenges, implementation work, and contributions from multiple people over time.

This repository represents the implementation that can currently be reproduced and verified from the surviving codebase.

Specific concepts, implementations, or contributions should be attributed according to the work actually represented in the relevant source code, documentation, research, or design material.

Earlier architectural concepts that are not represented by executable implementation in this repository remain part of the broader research context rather than being presented as completed functionality.

---

Repository Structure

The current implementation is organised around the following primary paths:

SWI-V1-Module-1-10/
├── README.md
├── SETUP_GUIDE.md
├── INSTALLATION.md
├── requirements.txt
├── .env.example
├── config/
│   └── swi_config.yaml
├── swi_core/
│   ├── __init__.py
│   ├── module00_trainer.py
│   ├── module01_node_scanner.py
│   ├── module02_security_probe.py
│   ├── module03_context_sync.py
│   ├── module04_encryption_handler.py
│   ├── module05_redaction_engine.py
│   ├── module06_drift_analyzer.py
│   ├── module07_memory_validator.py
│   ├── module08_access_auth.py
│   ├── module09_audit_logger.py
│   └── module10_external_sandbox.py
└── test_swi_core.py

The repository may also contain historical documents and supporting extraction/tooling files. The actual repository contents should remain authoritative as the implementation evolves.

---

Getting Started

1. Clone the repository

git clone https://github.com/Kelronmos/SWI-V1-Module-1-10.git
cd SWI-V1-Module-1-10

2. Create a virtual environment

python3 -m venv swi_env
source swi_env/bin/activate

On Windows:

swi_env\Scripts\activate

3. Install dependencies

pip install --upgrade pip
pip install -r requirements.txt

4. Run verification tests

python3 -m pytest test_swi_core.py -v

For the complete installation notes and working examples, see "INSTALLATION.md" and "SETUP_GUIDE.md".

Basic Pipeline Example

The current "AuditLogger" expects its log directory to exist before construction. The following example matches the documented interface:

import os
os.makedirs("logs", exist_ok=True)

from swi_core.module00_trainer import Trainer

trainer = Trainer(audit_log_path="logs/audit.jsonl")
result = trainer.process("Your input here")

print(f"Allowed: {result.allowed}")
print(f"Reason: {result.reason}")
print(f"Risk score: {result.security.risk_score}")
print(f"Redacted text: {result.redaction.redacted_text}")

Direct Context Validation Example

Because the Trainer interface does not currently accept timestamps, explicit timestamp validation is demonstrated through "ContextSync" directly:

import datetime
from swi_core.module03_context_sync import ContextSync

sync = ContextSync(staleness_seconds=1800.0)
result = sync.record_turn(
    1,
    timestamp=datetime.datetime.now(datetime.timezone.utc),
)

For additional module examples, use "INSTALLATION.md" and the test suite as the current implementation references.

---

Scope of Claims

This repository makes claims only about functionality supported by its current implementation and verification evidence.

The following should not be inferred merely from the existence of this repository:

- general intelligence;
- consciousness;
- semantic understanding;
- universal AI safety;
- complete cybersecurity;
- complete identity management;
- production-grade distributed enforcement;
- autonomous governance of arbitrary AI systems; or
- capabilities that existed only in earlier unrecovered development.

Where those concepts are relevant to broader SWI research, they should be treated as architectural, research, or historical context unless supported by current implementation and tests.

---

Guiding Principle

«Do not claim what the code cannot demonstrate.
Do not discard what has not yet been reconstructed.
Build from what can be proven, then extend from there.»

SWI is being rebuilt from a position of evidence.

The goal is not to preserve every historical claim.

The goal is to establish a foundation that can be inspected, tested, challenged, corrected, and extended.

---

License

See the repository's "LICENSE" file for the current terms governing use, modification, and distribution.
