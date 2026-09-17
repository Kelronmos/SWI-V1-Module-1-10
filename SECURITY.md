# Security Policy

## Reporting a Vulnerability

If you believe you have found a security vulnerability in SWI, please report it privately when public disclosure would expose an exploitable issue.

Preferred channel: open a **private** security advisory on this repository (GitHub Security Advisories), or contact the maintainers via the channels listed in the repository profile / Trusts Motion contact points.

Please include:

- affected module(s) or component(s);
- steps to reproduce;
- expected vs actual behaviour;
- any proof-of-concept (without unnecessary live exploit detail);
- your assessment of impact.

We aim to acknowledge reports promptly and to coordinate disclosure where a real vulnerability is confirmed.

---

## Classification Discipline

Not every concern is a vulnerability. Please distinguish:

| Category | Meaning |
|----------|--------|
| **Vulnerability** | Confirmed, exploitable weakness with evidence |
| **Design limitation** | Documented boundary of what the system claims to do |
| **Implementation defect** | Bug relative to a stated contract or test |
| **Documentation error** | Claim that does not match code or evidence |
| **Evidence gap** | Behaviour not yet covered by tests / CI / audit |
| **Theoretical concern** | Possible issue without demonstrated exploit path |
| **Confirmed exploit** | Reproduced attack against defined assumptions |

Do not label a design limitation or evidence gap as a vulnerability without supporting evidence.

---

## Scope Notes

- Sealed modules (M02, M03, M05, M06) have **bounded contracts**. A finding outside those contracts may be a limitation, not a broken seal.
- Foundation Seal 5 is **not ready**. Do not treat unsigned foundation evidence or local signatures as production security guarantees.
- Heuristic components (e.g. security probe patterns, bag-of-words drift) are not complete semantic defenses.

See `docs/KNOWN_LIMITATIONS.md` and module seal records for current honest scope.

---

## Safe Harbour for Good-Faith Research

Good-faith security research, testing against the public test suite, and responsible disclosure are welcome. Do not use findings to harm third parties or to misrepresent SWI status.

---

## Licence and Warranty

SWI is distributed under the Apache License 2.0 **AS IS**, without warranty. Reporting a vulnerability does not create any certification, SLA, or guarantee of fix timeline beyond good-faith response.
