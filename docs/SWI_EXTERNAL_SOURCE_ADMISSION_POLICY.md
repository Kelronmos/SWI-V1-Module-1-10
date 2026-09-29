# SWI External Source Admission Policy

**Status on first commit:** SPECIFIED  
**Not claimed:** IMPLEMENTED · TESTED · REPLAYABLE · PROVEN · SEALED · AUTHORIZED  
**Does not close:** FM-005–013 · Universal Gate · Foundation Seal 5  
**Legal/regulatory compliance:** NOT CLAIMED

> Named ≠ Implemented · Implemented ≠ Tested · Tested ≠ Sealed · Sealed ≠ Authorized.

---

## 1. Purpose

SWI may pull external source, but **source acquisition is not authorization**.

Every external source must pass provenance, licence/policy, integrity, security, privacy, and architecture-boundary checks before it can enter an executable or trusted path.

A detected violation causes **HALT** unless the violation is demonstrably fixed or an authorized, scoped exception exists.

This policy is the foundation contract for:

- Open-source licence obligations
- Privacy obligations when source or data carries personal data or processing constraints
- Protection of SWI architecture boundaries (privileged vs non-privileged placement)

---

## 2. Scope

Applies to any external:

- source code
- dependency / package
- repository
- artefact
- model or component
- configuration
- data source

when it is intended to enter a SWI formation, execution, or trusted path.

---

## 3. Core rules (non-negotiable)

| Rule | Meaning |
|------|---------|
| Pull ≠ trusted | Receiving material does not make it authorized |
| Scan ≠ approved | Completing a scanner run is not admission |
| Warning ≠ authorization | A warning must not be treated as a pass |
| Hash ≠ authority | Integrity digest proves correspondence to content, not legal permission, safety, or authorization |
| Violation → HALT | Controlled operation must not proceed |
| Fix → revalidation | Metadata edits alone do not convert HALT to PASS |
| Exception → explicit + scoped | Authorization must be recorded; it does not erase the original violation |
| Missing evidence → HALT / NOT_PROVEN | Absence of required evidence is not a pass |

---

## 4. Lifecycle (geometry)

```
EXTERNAL SOURCE
      ↓
PULL / RECEIVE
      ↓
QUARANTINE
      ↓
IDENTIFY
  ├─ origin
  ├─ version / commit
  ├─ license
  ├─ dependencies
  └─ integrity
      ↓
POLICY CHECK
  ├─ privacy obligations
  ├─ open-source obligations
  ├─ security
  └─ architecture boundaries
      ↓
      ├───────────────┐
      ↓               ↓
    PASS          VIOLATION
      ↓               ↓
   ADMIT          WARNING / HALT
                      ↓
             ┌────────┴────────┐
             ↓                 ↓
          FIXED          AUTHORIZED
             ↓                 ↓
          RECHECK          EXCEPTION (scoped)
             └────────┬────────┘
                      ↓
                    ADMIT
```

A violation must never silently transition:

```
VIOLATION → ADMITTED
```

It must go through FIX or EXPLICIT AUTHORIZATION, then REVALIDATE, then a new decision.

---

## 5. Check layers

### 5.1 Provenance

- Where did it come from?
- Who published it?
- What exact version / immutable reference?
- Can the origin be established?

Unknown or unverifiable provenance → **HALT** (or WARNING only if policy explicitly allows review queue, never automatic ADMIT).

### 5.2 Integrity

- Canonical representation → SHA-256 → recorded hash

**HASH ≠ AUTHORITY.**  
A valid hash proves the recorded material matches that digest. It does not prove legal permission, trustworthiness, safety, licence compliance, or authorization.

### 5.3 Licence (open-source obligations)

- Licence identified?
- Licence source known?
- Obligations known (attribution, copyleft, notice, patent grants, etc.)?
- Intended use compatible with SWI architecture and distribution model?

Unknown licence → **HALT**.  
Do not infer “public repository = permission” or “GitHub = open source”.

### 5.4 Privacy

When the source or accompanying data may involve personal data or processing constraints:

- Purpose limitation and data minimisation concepts must be considered
- Lawful basis / necessity questions are recorded as checks, not as compliance certificates
- Privacy violation or unresolved privacy obligation → **HALT** or scoped exception only

This policy references privacy law principles (e.g. purpose limitation, minimisation) as **design constraints**. It does **not** claim GDPR, CCPA, or any other regime is satisfied.

### 5.5 Security

Known malicious patterns, unresolved critical vulnerabilities, or policy-banned components → **HALT**.

### 5.6 Architecture boundary

The same external component can receive different decisions by target boundary:

| Target boundary | Example decision |
|-----------------|------------------|
| Documentation / non-executable | PASS possible |
| Development dependency | PASS or REVIEW |
| Production dependency | REVIEW |
| Privileged SWI execution path | HALT unless all required checks pass |

Architecture laundering (approved for one boundary, used in a higher privilege boundary without revalidation) → **HALT**.

---

## 6. Decision and HALT behaviour

```
decision = evaluate_source(source)

if decision.status == "HALT":
    record_halt(decision)
    quarantine(source)
    raise SourceAdmissionHalt(decision)   # operation must not proceed
```

The critical test is not “did SWI write HALT to a log?”  
It is: **“Did the prohibited operation actually fail to proceed (zero protected side-effect)?”**

Decision layer ≠ execution enforcement. Both are required before any claim of TESTED enforcement.

---

## 7. Evidence record (minimum fields)

Every important transition should be recordable and later replayable:

- source_id, origin, version, immutable_reference
- provenance, integrity (algorithm + content_hash)
- licence identifier and obligations
- policy_checks, security_checks, privacy_checks, architecture_checks
- violations[], warnings[]
- decision, decision_basis
- authorization (if any) — scoped, never erases original violation
- remediation (if any)
- revalidation result
- evidence_hash
- status (e.g. NOT_PROVEN until higher evidence exists)

Do **not** put `approved: true` solely because a scanner completed.

Distinguish:

- CHECK_COMPLETED
- CHECK_PASSED
- AUTHORIZED
- ADMITTED
- EXECUTED

Those are different facts.

---

## 8. What this policy may record vs must not claim

**Recordable facts (when demonstrated):**  
SOURCE RECEIVED · HASH CALCULATED · LICENCE IDENTIFIED · CHECK EXECUTED · VIOLATION DETECTED · HALT ISSUED · OPERATION BLOCKED · FIX APPLIED · REVALIDATION EXECUTED · AUTHORIZATION PRESENT · EVIDENCE HASH · REPLAY RESULT

**Must not automatically claim:**  
“safe” · “trusted” · “legal” · “compliant” · “secure” · “authorized” · “production-ready” · “universally governed” · “proven” · GDPR/CCPA/AI-Act compliance

---

## 9. Relationship to existing residuals

This policy does **not** close FM-005 through FM-013.  
Those residuals remain OPEN in `docs/formation_path_inventory.json` until independent evidence shows otherwise.

Universal Gate remains **NOT_PROVEN**.  
Foundation Seal 5 remains **NOT READY**.  
Legal/regulatory compliance remains **NOT CLAIMED**.

---

## 10. Status model for this control

```
NAMED
  ↓
SPECIFIED          ← this document
  ↓
IMPLEMENTED        ← code + models + halt path
  ↓
TESTED             ← violation → HALT → zero side-effect demonstrated
  ↓
REPLAYABLE         ← same evidence → same decision
  ↓
INDEPENDENTLY VERIFIED
  ↓
PROVEN WITHIN SCOPE
  ↓
SEALED
```

On first commit of this file, the control is **SPECIFIED only**.

---

## 11. Machine decision sketch (non-normative until implemented)

```
if source.violation:
    HALT
elif source.fixed:
    revalidate(source)
elif source.authorized_exception:
    record_authorization()
    continue  # only within recorded scope
elif all_required_checks_pass:
    ADMIT
else:
    HALT
```

Every HALT should leave an evidence trail (source identity, rule, detection, action=HALT, evidence_hash).

---

**End of policy document.**  
Implementation, tests, and replay evidence are separate work items and must not be assumed from the existence of this file.
