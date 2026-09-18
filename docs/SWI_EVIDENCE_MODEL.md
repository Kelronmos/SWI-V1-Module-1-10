# SWI Evidence Model

**Status:** SPECIFICATION  
**Rule:** MODEL EXPLANATION ≠ AUDIT EVIDENCE  

LLM or narrative explanation may be stored as **context**. It does not become
authoritative evidence without an explicit evidence type and verification path.

## Evidence kinds (conceptual)

| Kind | Role |
|------|------|
| IdentityEvidence | Who is asserted |
| AuthorityEvidence | What authority was presented |
| PolicyEvidence | Which policy/version applied |
| ContextEvidence | Situational inputs (incl. free text) |
| SourceEvidence | Provenance of data |
| ExecutionEvidence | What ran |
| OutcomeEvidence | What resulted |
| IntegrityEvidence | Digests / chains / signatures |

## Live producer (V1)

`FoundationEvidenceEnvelope` from `swi_core.foundation_evidence` is **IntegrityEvidence**
for pipeline outcomes under a versioned schema — not factual-truth evidence.
