# Foundation Milestone — What “Done” Means for Modules 00–10

This is **not** “10 modules that work.”  
It is a foundation that can **prove** what it does, **detect** when something is wrong, and **stop** rather than quietly continue.

## 1. Every module has a defined contract

For each module you should answer:

- What goes in?
- What does it do?
- What comes out?
- What can make it fail?
- What does it refuse to accept?
- What tests prove it?

No vague “AI intelligence” claims.

## 2. Security is part of the execution path

```text
Input → PRE-CHECK → MODULE → POST-CHECK → HANDOFF
```

Pre-check fails → **STOP**  
Invalid module result → **STOP**  
Post-check fails → **STOP**  

The next module does not trust the previous module merely because something was returned.

**Current status:** Module 02 is on this path. Other modules still need kernel migration.

## 3. The 00–10 pipeline is auditable

Target flow:

```text
00 Trainer → 02 (kernel) → 03 → 05 → 06 → 07 → 09
```

When something stops, you should know **where** and **why**.  
Trainer records a halt reason when Module 02’s kernel fails, then re-raises.

## 4. Tests are evidence, not decoration

Run:

```bash
python -m pytest -q
./scripts/verify.sh
```

You must know what those tests prove — and what they do **not** prove.  
See `docs/EVIDENCE_MATRIX.md` and `docs/KNOWN_LIMITATIONS.md`.

## 5. CI catches regression

```text
Code change → tests → doc/claim checks → PASS merge / FAIL investigate
```

A workflow **file** is not proof. A green Actions run is proof.

## 6. Documentation does not outrun the code

| Category | Meaning |
|----------|---------|
| **IMPLEMENTED + TESTED** | In the repo; automated tests demonstrate it |
| **ARCHITECTURAL / PLANNED** | Design direction; not implemented yet |
| **HISTORICAL / RESEARCH** | Earlier SWI work retained for reference |

CEK, SAD-DFU, Vector Memory, Sovereign Mesh, anticipatory mechanisms stay out of the first column until code + tests exist.

## 7. A future contributor can rebuild it

Someone joining later should find implementation, tests, limitations, and evidence without a private walkthrough.  
Start: `docs/START_HERE.md`.

## 8. Fail visibly

Preferred:

```text
Something went wrong → CHECK FAILED → STOP → record reason → human review if needed
```

Not:

```text
Something went wrong → keep going → answer anyway → pretend fine
```

## 9. This is not the entire SWI vision

Finishing 00–10 with verification does **not** mean AGI, universal safety, solved hallucinations, or a live sovereign mesh.

It means:

> A verified foundation from which those future questions can be investigated honestly.

## Milestone statement (when Seal 5 is earned)

> I don't need you to believe me. Here is the code. Here are the tests. Here are the results. Here are the limitations. Here is what has not yet been built.

Until Seal 5, treat every larger claim as architectural or historical.
