---------------------------- MODULE SWIWorkflowV47 ----------------------------
(***************************************************************************)
(* SWI V4.7 abstract gated workflow model                                  *)
(*                                                                         *)
(* Properties:                                                             *)
(*   W1  formed => admitted                                                *)
(*   W2  ~admitted => auditWrites = 0                                      *)
(*   W3  rejected => ~formed                                               *)
(*                                                                         *)
(* NON-CLAIMS:                                                             *)
(*   - Does not prove the Python implementation obeys this model           *)
(*   - Does not close FM-005                                               *)
(*   - Does not establish Universal Gate                                   *)
(*   - Result is at most PROVEN_ON_MODEL                                   *)
(***************************************************************************)

EXTENDS Naturals

CONSTANT MaxTurns

VARIABLES
  phase,
  admitted,
  formed,
  rejected,
  auditWrites,
  turn

vars == <<phase, admitted, formed, rejected, auditWrites, turn>>

TypeOK ==
  /\ phase \in {"Idle", "Admitted", "Formed", "Halted", "Rejected"}
  /\ admitted \in BOOLEAN
  /\ formed \in BOOLEAN
  /\ rejected \in BOOLEAN
  /\ auditWrites \in Nat
  /\ turn \in 0..MaxTurns

Init ==
  /\ phase = "Idle"
  /\ admitted = FALSE
  /\ formed = FALSE
  /\ rejected = FALSE
  /\ auditWrites = 0
  /\ turn = 0

Admit(ok) ==
  /\ phase = "Idle"
  /\ admitted' = ok
  /\ rejected' = ~ok
  /\ phase' = IF ok THEN "Admitted" ELSE "Rejected"
  /\ UNCHANGED <<formed, auditWrites, turn>>

Form ==
  /\ phase = "Admitted"
  /\ admitted
  /\ ~rejected
  /\ turn < MaxTurns
  /\ formed' = TRUE
  /\ turn' = turn + 1
  /\ auditWrites' = auditWrites + 1
  /\ phase' = "Formed"
  /\ UNCHANGED <<admitted, rejected>>

Halt ==
  /\ phase \in {"Admitted", "Formed"}
  /\ phase' = "Halted"
  /\ UNCHANGED <<admitted, formed, rejected, auditWrites, turn>>

RejectedStutter ==
  /\ phase = "Rejected"
  /\ UNCHANGED vars

Next ==
  \/ \E ok \in BOOLEAN : Admit(ok)
  \/ Form
  \/ Halt
  \/ RejectedStutter

Spec == Init /\ [][Next]_vars

W1_FormedRequiresAdmission ==
  formed => admitted

W2_NoAuditBeforeAdmission ==
  (~admitted) => auditWrites = 0

W3_RejectedCannotForm ==
  rejected => ~formed

THEOREM TypeSafety ==
  Spec => []TypeOK

=============================================================================
