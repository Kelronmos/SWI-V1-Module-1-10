# Contributing to SWI

SWI is open for collaboration.

Collaboration does **not** rewrite provenance.

Permission is **not** required to contribute.  
Evidence **is** required before claims are accepted.

---

## Philosophy

> Open the code, not the history.

You may improve modules, fix flaws, add tests, propose new modules, port implementations, or build research variants.  
Your contribution will be credited.  
It will not become the origin of SWI itself.

---

## How to Contribute

1. Open an issue describing the problem or proposal (preferred for non-trivial changes).
2. Fork the repository.
3. Create a focused branch.
4. Implement the change with tests.
5. Ensure the test suite and verification scripts pass:
   ```bash
   python -m pytest -q
   ./scripts/verify.sh
   ```
6. Submit a pull request with a clear description of:
   - what changed,
   - why,
   - how it was tested,
   - any limitations.

Small, well-tested changes are preferred over large untested ones.

---

## Evidence Before Claims

SWI follows this discipline:

**Claim → Implementation → Test → Result → Limitation → Next Iteration**

Contributors must distinguish between:

1. **Proposed** behaviour  
2. **Implemented** behaviour  
3. **Tested** behaviour  
4. **CI-verified** behaviour  
5. **Audited** behaviour  
6. **Sealed** behaviour  
7. **Independently verified** behaviour

A documentation statement does not establish implementation.  
A passing test does not establish universal correctness.  
A cryptographic signature does not establish factual truth.  
A successful CI run does not establish production security.

**Do not** represent experimental, proposed, partially implemented, or failed capabilities as established SWI functionality.

---

## Code and Test Requirements

- Changes that alter module behaviour or contracts should include corresponding tests.
- Prefer small, reviewable diffs.
- Keep the existing honesty standard: document limitations explicitly.
- Do not weaken sealed contracts (M02, M03, M05, M06) without clear evidence and discussion.
- Foundation Seal 5 and higher modules remain gated by the project’s evidence rules.

---

## Attribution Rules

- Contributors retain recognition for their original contributions.
- The original SWI architecture and project identity remain attributed to Keletso Ronald Mosidila / Trusts Motion.
- When documenting your work, distinguish:
  - original SWI design and evidence chain,
  - your contribution,
  - any independent or alternative implementation.

Forks, ports, research implementations, and derivative works should not be presented as the original SWI project or as work authored by the original SWI authors unless that attribution is accurate.

---

## No-Overclaiming Policy

Contribution to SWI does **not** constitute:

- endorsement by the original author or Trusts Motion,
- certification that SWI is secure, safe, or production-ready,
- authority to speak on behalf of the project,
- permission to rewrite project history or provenance.

Seals, evidence envelopes, and technical status statements remain governed by the repository’s evidence rules and documentation, not by authorship of any single contribution.

---

## Trademarks and Project Identity

The Apache License 2.0 does **not** grant trademark rights.

"SWI", "Structured Workflow Intelligence", "Trusts Motion", and related marks identify the original project.  
Please do not use these names in a way that creates confusion about the source or official status of a modified or independent work.

Truthful technical references ("compatible with SWI", "based on the SWI pipeline", academic citations) are fine.  
Presenting a fork or commercial product as the official SWI project is not.

See `NOTICE` and `AUTHORS_AND_LEGACY.md` for further context.

---

## Licence of Contributions

By submitting a contribution, you agree that your contribution is provided under the terms of the Apache License 2.0, unless you explicitly state otherwise in the pull request.

---

## Questions

Open an issue. Serious technical discussion is welcome.

Thank you for helping improve SWI while keeping its history and evidence standards intact.
