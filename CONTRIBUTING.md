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

Governing technical doctrine:

> EVIDENCE BEFORE CLAIM.  
> BOUNDARY BEFORE EXPANSION.  
> CONTRACT BEFORE IMPLEMENTATION.  
> TEST FOR BEHAVIOUR.  
> CI FOR REPRODUCIBILITY.  
> AUDIT FOR CONFIDENCE.  
> SEAL FOR CONTROLLED DEPENDENCY.

---

## Contribution workflow

```text
Issue / Proposal
      ↓
Understand boundary
      ↓
Define claim
      ↓
Implement
      ↓
Write tests
      ↓
Run tests
      ↓
Document result
      ↓
Document limitation
      ↓
CI
      ↓
Review
      ↓
Merge
```

Do not begin by claiming the result. Begin by defining what you intend to demonstrate.

---

## Pull request standard

Every technical PR should state:

### Claim
What property is this change intended to demonstrate?

### Implementation
What code changed?

### Tests
What tests were added or changed?

### Result
What actually happened?

### Limitation
What remains unproven?

### CI
Which CI run demonstrates reproducibility (if available)?

### Risk
What existing behaviour could this affect?

### Evidence
What repository evidence supports the claim?

---

## Evidence Before Claims

**Claim → Implementation → Test → Result → Limitation → Next Iteration**

For stronger claims:

Claim → Code → Test → CI → Audit → Seal → Independent verification

Contributors must distinguish:

1. **Proposed**  
2. **Implemented**  
3. **Tested**  
4. **CI-verified**  
5. **Audited**  
6. **Sealed**  
7. **Independently verified**

A documentation statement does not establish implementation.  
A passing test does not establish universal correctness.  
A cryptographic signature does not establish factual truth.  
A successful CI run does not establish production security.

**Do not** represent experimental, proposed, partially implemented, or failed capabilities as established SWI functionality.

---

## What contributors must not claim

Something is not “established” merely because:

- it exists in documentation;
- a function exists;
- one test passes;
- a local run succeeds;
- a signature verifies;
- a hash matches;
- CI is green;
- one experiment succeeded.

---

## Code and test requirements

- Changes that alter module behaviour or contracts should include corresponding tests.
- Prefer small, reviewable diffs.
- Keep the honesty standard: document limitations explicitly.
- Do not weaken sealed contracts (M02, M03, M05, M06) without clear evidence and discussion.
- Foundation Seal 5 and higher modules remain gated by the project’s evidence rules.
- Collaboration / licence documentation changes must not modify M11 seals, M12 contracts, or cryptographic evidence artefacts.

---

## Review checklist (for reviewers)

- **Boundary** — Does the change stay inside the module’s responsibility?
- **Contract** — Does implementation match the contract?
- **Tests** — Do tests assert the property being claimed?
- **Failure behaviour** — Does invalid input fail correctly?
- **Regression** — Could the change break an earlier module?
- **Evidence** — Can another person reproduce the result?
- **Overclaiming** — Does documentation say more than the implementation proves?

---

## Attribution rules

- Contributors retain recognition for their original contributions.
- The original SWI architecture and project identity remain attributed to Keletso Ronald Mosidila / Trusts Motion.
- Distinguish: original SWI design and evidence chain · your contribution · independent or alternative implementation.

Forks, ports, research implementations, and derivative works should not be presented as the original SWI project or as work authored by the original SWI authors unless that attribution is accurate.

Contribution does **not** constitute endorsement, certification, employment, partnership, or authority to speak on behalf of Trusts Motion.

---

## Independent implementations and language ports

Independent implementations are welcome. They are not automatically “the official SWI implementation.”

Language ports should follow:

```text
Reference contract → Reference tests → Conformance requirements
      → New-language implementation → Conformance tests
      → Comparison → Document differences
```

Python remains the reference implementation unless the project deliberately changes that designation.

---

## Security reports

See [SECURITY.md](SECURITY.md). Prefer private disclosure for exploitable issues. Distinguish vulnerability, design limitation, defect, documentation error, and evidence gap.

---

## Trademarks and project identity

The Apache License 2.0 does **not** grant trademark rights.

"SWI", "Structured Workflow Intelligence", "Trusts Motion", and related marks identify the original project.  
Truthful technical references are fine. Presenting a fork or commercial product as the official SWI project is not.

See `NOTICE` and `AUTHORS_AND_LEGACY.md`.

---

## Licence of contributions

By submitting a contribution, you agree that your contribution is provided under the Apache License 2.0, unless you explicitly state otherwise in the pull request.

---

## Questions

Open an issue. Serious technical discussion and failure reports are welcome.

A failure report is valuable evidence.

Thank you for helping improve SWI while keeping its history and evidence standards intact.
