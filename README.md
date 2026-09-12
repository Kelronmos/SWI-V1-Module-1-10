Structured Workflow Intelligence (SWI)

Modules 00–10 — Verified Reference Implementation

Author: Keletso Ronald Mosidila
Organisation: Trusts Motion
Status: Active Reconstruction / Verified Reference Implementation

---

What This Repository Is

This repository contains the currently verified implementation of the SWI Modules 00–10 reference implementation.

It establishes a local, single-process, reproducible engineering foundation for components that can currently be demonstrated through source code, executable tests, and documented behaviour.

This repository is not a complete reconstruction of the broader SWI architecture or of every capability, prototype, research direction, or architectural concept previously explored under SWI.

«What is implemented must be distinguishable from what is remembered, proposed, or intended.»

---

Verification Boundary

The current repository should be evaluated from the code, tests, and documented behaviour rather than from architectural claims alone.

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

The current repository establishes a verified implementation foundation for the Modules 00–10 reference implementation.

It provides a local, single-process workflow in which Module 00 — Trainer is the primary orchestrator for the modules currently wired into its execution path.

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

Standalone Components

The following modules are implemented in the repository but are not directly invoked by Module 00's default execution path:

- Module 01 — SHA-256 Node Scanner
- Module 04 — AES-256-GCM Encryption
- Module 08 — Access Authentication / Tokens
- Module 10 — External Sandbox

A module existing in the repository does not automatically mean that it is part of the default execution path.

---

Module Overview

Module| Component| Current Role
00| Trainer| Pipeline orchestration
01| Node Scanner| SHA-256 integrity scanning
02| Security Probe| Instruction/injection risk detection
03| Context Sync| Timestamp and ordering validation
04| Encryption| AES-256-GCM encryption utility
05| Redaction| Sensitive-content handling
06| Drift Detection| Context/drift analysis
07| Memory Validator| Memory consistency validation
08| Access Auth| Authentication/token handling
09| Audit Logger| Audit/event recording
10| External Sandbox| External execution boundary

---

Implementation Boundaries

This repository is a reference implementation of specific workflow, integrity, security, validation, and audit mechanisms.

It should not be represented as a complete autonomous AI governance system.

Module 06 — Drift Detection

The current drift mechanism uses a coarse syntactic approach.

It should not be described as semantic understanding, consciousness, reasoning about meaning, or proof that a system understands context.

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

Testing

Tests demonstrate the behaviour covered by the current implementation.

They are not evidence of capabilities outside their coverage.

The repository includes module-level checks covering areas such as:

- node integrity and tamper detection;
- instruction-override/injection detection;
- context ordering and staleness;
- redaction behaviour;
- drift handling;
- memory validation; and
- audit logging.

Run the current test suite with:

python3 -m pytest test_swi_core.py -v

For coverage reporting, the repository also provides Makefile targets:

make test

and:

make coverage

See the repository's setup and installation documentation for environment requirements and additional instructions.

---

Evidence and Verification

The implementation should be evaluated through the following chain:

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

A passing test demonstrates the behaviour exercised by that test.

It does not establish that the entire SWI architecture, or any capability outside the test's coverage, has been proven.

This distinction is central to the reconstruction.

---

Integrity Terminology

This project uses tamper-evident rather than tamper-proof terminology.

A tamper-evident mechanism is intended to detect or expose alteration.

It does not imply that alteration is impossible.

Likewise, tested means that the relevant automated tests pass under the conditions covered by those tests.

It does not mean that the entire system is universally proven secure, correct, or complete.

---

Architectural Continuity

SWI has developed through research, experimentation, architectural discussion, and implementation across multiple stages.

Earlier work explored deeper semantic, kernel-level, and higher-order architectural concepts. Those directions remain part of the broader SWI research context.

They are not presented here as implemented capabilities unless they can be reconstructed, implemented, tested, and verified.

This repository is therefore not a replacement for the broader SWI architecture.

It is the verified implementation layer being rebuilt from surviving, reproducible evidence.

«Architecture describes where SWI is intended to go.
Implementation demonstrates what SWI can currently prove.»

The absence of a concept from this repository does not mean that the concept was abandoned.

Likewise, mentioning an architectural concept does not mean that it has been implemented.

---

Reconstruction Principle

Earlier SWI development grew beyond what is currently preserved in this repository.

Some capabilities can still be remembered or described, while the surviving code may not be sufficient to reproduce or prove them.

The rebuild therefore does not attempt to recreate missing functionality simply because it is remembered.

Instead:

- surviving code is inspected;
- behaviour is reproduced;
- tests are written or executed;
- limitations are documented;
- architectural concepts remain clearly labelled; and
- new implementation is added only when it can be verified.

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

The repository is organised around the current reference implementation and its verification materials.

The primary implementation is located under:

swi_core/

The main test suite is:

test_swi_core.py

Supporting documentation and tooling include:

SETUP_GUIDE.md
INSTALLATION.md
Makefile
quickstart.sh
extract_and_setup.py

The exact repository structure should be treated as authoritative over this overview as the implementation evolves.

---

Getting Started

Install the required Python dependencies according to the repository setup documentation.

Then run:

python3 -m pytest test_swi_core.py -v

For the standard Makefile test target:

make test

For coverage:

make coverage

For a guided setup, review:

SETUP_GUIDE.md

and:

INSTALLATION.md

---

Scope of Claims

This repository makes claims only about functionality that can be supported by its current implementation and verification evidence.

The following should not be inferred merely from the existence of the repository:

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

See the repository license for the current terms governing use, modification, and distribution.
