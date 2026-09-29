# SWI Reference Policy

**Status:** PROTOTYPE documentation only  
**Production citation layer:** NOT_IMPLEMENTED  
**Independent reference verification:** NOT_CLAIMED  
**Production authority from citations:** NOT CLAIMED

## Core distinctions

```
REFERENCE ≠ AUTHORITY
CITATION ≠ AUTHORITY
LINK ≠ PROOF
DOCUMENTATION ≠ EXECUTION
SOURCE CODE ≠ AUTHORITY
HASH ≠ AUTHORITY
HASH ≠ TRUTH
POLICY-ON-PAPER ≠ ENFORCEMENT
DECISION ≠ EXECUTION
EVIDENCE ≠ AUTHORITY ≠ DECISION ≠ EXECUTION
```

A reference establishes **traceability** (where material was pointed at).  
It does **not** establish truth, authorization, legal standing, or production trust.

## Repository link standard

Use ordinary Markdown only:

```markdown
[SWI V1](https://github.com/Kelronmos/SWI-V1-Module-1-10)
[Structured Workflow Intelligence](https://github.com/Kelronmos/Structured-Workflow-Intelligence)
```

Do **not** place conversation-interface metadata in repository files:

- ChatGPT private-use citation markers
- `turnNsearch` / `turnNnews` / `turnNview` identifiers
- `utm_source=chatgpt.com` tracking parameters on links
- Fabricated destinations

If a destination cannot be verified: write *Reference destination not currently verified.* — do not invent a URL.

## Future production reference layer (design only — NOT IMPLEMENTED)

```
SOURCE → IDENTIFY → VERSION → VERIFY → RECORD → HASH → CITE → REPLAY
```

Requirements before any production claim:

1. Source identity  
2. Source version  
3. Retrieval timestamp  
4. Immutable reference  
5. Content hash where applicable  
6. Provenance  
7. Citation record  
8. Replay verification  
9. Source-change detection  
10. Authority separation  
11. Independent verification  
12. Failure / withdrawal mechanism  

This list is a **roadmap**, not an implemented system.

## Discipline reminder

```
UNKNOWN ≠ FALSE
QUESTION ≠ DENY
REVIEW ≠ FAILURE
PASS ≠ UNIVERSAL AUTHORITY
SEALED ≠ PRODUCTION TRUST
PROTOTYPE ≠ PRODUCTION
```
