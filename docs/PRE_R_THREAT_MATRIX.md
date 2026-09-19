# pre-R Boundary Threat Matrix

**Status:** DESIGN (no executable evidence)  
**Date:** 2026-09-19  

| Threat | Boundary | Expected | Evidence |
|--------|----------|----------|----------|
| Wrong request | Binding | REJECT | — |
| Wrong recipient | Destination | REJECT | — |
| Authority expansion | Authority | REJECT | — |
| UI injection | Presentation | REJECT / void | — |
| Backend injection | Backend | REJECT | — |
| Evidence removal | Evidence | REJECT | — |
| Hash alteration | Integrity | REJECT | — |
| Replay (if single-use) | Lifecycle | REJECT | — |
| Expiry bypass | Lifecycle | REJECT | — |
| Certificate substitution | Evidence | REJECT | — |
| Key substitution | Crypto | REJECT / HALT | — |
| Unknown authority | Authority | HALT / REJECT | — |
| Automatic privileged action | Action | BLOCKED | — |
| Authority laundering | Authority | REJECT | — |
| Transform inherits trust | Transform | REJECT | — |
