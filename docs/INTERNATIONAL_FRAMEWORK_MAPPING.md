# International Framework Mapping (Technical Alignment Only)

**Not legal compliance. Not certification. Not an audit opinion.**

Regenerate machine-readable form via:

```bash
python scripts/swi_validation_harness.py
```

## Defensible overall statement

> SWI is developing a security and workflow-integrity architecture with demonstrable alignment to several *technical control themes* in contemporary AI governance frameworks. Significant areas—including universal enforcement, lifecycle risk management, impact assessment, fairness, data governance, and independent conformity assessment—remain open or unproven.

## Framework snapshot

| Framework | Strongest SWI overlap | Gaps |
|-----------|----------------------|------|
| EU AI Act | Logging/traceability direction; oversight-shaped admission; adversarial robustness tests | Art. 9 full RMS; Art. 10 data/bias; conformity assessment |
| UN A/RES/78/265 | Testing, vulnerability focus, provenance direction | Impact assessment, international interoperability proof |
| UNESCO AI Ethics | Accountability, oversight, security themes | Fairness, non-discrimination, environmental/social impact |
| Council of Europe AI Convention | Structural authorization integrity | Human-rights impact assessment path |
| NIST AI RMF | Secure/accountable/transparent characteristics | Fairness, privacy-enhanced, explainability depth |

## Universal Gate note

International alignment **increases** the importance of:

```text
∀ formation paths → admission.valid
```

Trainer/export/sign gates are necessary but not sufficient while direct module APIs and `ModuleKernel(require_admission=False)` remain residual bypasses.

**Universal Gate = NOT PROVEN**

## Status of this document

| Field | Value |
|-------|--------|
| Module 10 | PROPOSED / NOT ADMITTED |
| Foundation Seal 5 | NOT READY |
| Package | 0.1.0a1 Alpha |
| Compliance certificate | **None** |
