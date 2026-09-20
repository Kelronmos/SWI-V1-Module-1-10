---------------------------- MODULE SWIWorkflow001 ----------------------------
(***************************************************************************)
(* SWI-WORKFLOW-001  — Abstract gated workflow model                       *)
(*                                                                         *)
(* Property: formed => admitted                                            *)
(* Class:    Safety invariant                                              *)
(* Scope:    Abstract model only                                           *)
(*                                                                         *)
(* NON-CLAIMS:                                                             *)
(*   - Does not prove the Python implementation obeys this model           *)
(*   - Does not close FM-005                                               *)
(*   - Does not establish Universal Gate                                   *)
(*   - Does not seal mathematics or production code                        *)
(*   - Result is at most PROVEN_ON_MODEL                                   *)
(***************************************************************************)

EXTENDS Naturals

CONSTANT MaxTurns

VARIABLES
  phase,       \* "Idle", "Admitted", "Formed", "Halted", "Rejected"
  admitted,    \* BOOLEAN
  formed,      \* BOOLEAN
  turn,        \* Nat
  auditWrites  \* Nat  (counts durable side effects)

vars == <<phase, admitted, formed, turn, auditWrites>>

TypeOK ==
  /\ phase \in {"Idle", "Admitted", "Formed", "Halted", "Rejected"}
  /\ admitted \in BOOLEAN
  /\ formed \in BOOLEAN
  /\ turn \in 0..MaxTurns
  /\ auditWrites \in Nat

Init ==
  /\ phase = "Idle"
  /\ admitted = FALSE
  /\ formed = FALSE
  /\ turn = 0
  /\ auditWrites = 0

Admit(ok) ==
  /\ phase = "Idle"
  /\ admitted' = ok
  /\ phase' = IF ok THEN "Admitted" ELSE "Rejected"
  /\ UNCHANGED <<formed, turn, auditWrites>>

\* Formation ONLY from Admitted (gated)
Form ==
  /\ phase = "Admitted"
  /\ admitted = TRUE
  /\ turn < MaxTurns
  /\ formed' = TRUE
  /\ turn' = turn + 1
  /\ auditWrites' = auditWrites + 1
  /\ phase' = "Formed"
  /\ UNCHANGED admitted

Halt ==
  /\ phase \in {"Admitted", "Formed"}
  /\ phase' = "Halted"
  /\ UNCHANGED <<admitted, formed, turn, auditWrites>>

RejectIdle ==
  /\ phase = "Rejected"
  /\ UNCHANGED vars

Next ==
  \/ \E ok \in BOOLEAN : Admit(ok)
  \/ Form
  \/ Halt
  \/ RejectIdle

Spec == Init /\ [][Next]_vars

\* --- Safety Properties ---

SafeFormation == formed => admitted

NoAuditBeforeAdmit == (~admitted) => auditWrites = 0

RejectCannotForm == (phase = "Rejected") => ~formed

=============================================================================
