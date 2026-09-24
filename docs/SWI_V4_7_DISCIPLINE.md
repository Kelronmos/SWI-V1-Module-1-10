# Structured Workflow Intelligence (SWI) V4.7 Discipline

**Status:** MAPPED / SPECIFIED  
**Purpose:** repository construction discipline and evidence-boundary reference.

## 1. Identity

The canonical name is **Structured Workflow Intelligence (SWI)**.

Use SWI consistently in architecture, verification, evidence, module mapping, and repository documentation.

## 2. Evidence vocabulary

### Architecture states

`PROPOSED → MAPPED → SPECIFIED → IMPLEMENTED → TESTED → ADVERSARIALLY_TESTED → REPLAY_VERIFIED → EVIDENCE_HASHED → SEALED`

### Formal-result states

`PROVEN_ON_MODEL | PROVEN | FALSIFIED | NOT_PROVEN | BOUND_ONLY`

### Residual states

`OPEN | CLOSED | INAPPLICABLE`

A status must be earned by corresponding evidence.

## 3. Boundary law

The following are separate evidence tracks:

`Vector Math ≠ TLA+ ≠ S9 Graph ≠ Static ≠ Runtime ≠ Refinement`

Evidence does not migrate automatically between tracks.

A TLA+ invariant may establish a model property. It does not, without a separate correspondence argument, establish that the implementation obeys the model.

## 4. Truth labels

- **SIMULATED:** behavior is represented but the claimed real boundary is absent.
- **PARTIAL:** a real portion exists, but required closure conditions are missing.
- **VERIFIED:** a specified verification procedure has actually been executed and its scope is documented.
- **SEALED:** the repository's defined seal criteria have been met and evidence is immutable/replayable according to that repository's contract.

Do not use `VERIFIED` as a synonym for `SEALED`.

## 5. Non-claims

Every evidence envelope must state what it does not prove.

At minimum, formal evidence must not silently become:

- production-code proof
- authorization
- execution permission
- legal compliance
- standing
- cryptographic root of trust
- Universal Gate
- mathematical seal

## 6. Frozen-state rule

If an implementation is declared frozen, verification work must reference its exact full SHA. New evidence belongs to a new verification track or branch unless the change is explicitly part of a controlled rebuild.

## 7. Module mapping

A module number can identify where future construction belongs. It does not mean the module exists, is complete, or is sealed.

## 8. Evidence identity

Human-facing filenames may use short SHAs. Machine evidence must carry the full source SHA.

## 9. Decision rule

If the evidence cannot demonstrate the claimed boundary, downgrade the claim rather than strengthening the label.
