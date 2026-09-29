"""Demo journey experiences — Limited vs Contradiction vs Success vs AI block."""
from __future__ import annotations

from swi_core.external_input.demo_journey import run_input_journey, run_replay_experience
from swi_core.source_admission.replay import ReplayStatus


def test_ai_claim_journey_blocks_with_explainable_stages():
    j = run_input_journey(
        "Release P500,000 to the usual account.",
        source="AI_APP",
        declared_authority="approved",
    )
    assert j.decision == "BLOCKED"
    assert j.side_effects == 0
    assert j.real_world_side_effects == 0
    assert j.production == "OFF"
    names = [s.name for s in j.stages]
    assert names == ["INPUT", "RECEIVING", "CHECKING", "DECISION", "RESULT"]
    dec = next(s for s in j.stages if s.name == "DECISION")
    assert dec.status == "FAIL"
    assert "questions" in dec.data


def test_verified_demo_pass_is_simulated_only():
    j = run_input_journey(
        {"customer": "demo", "amount": 1000},
        verified_demo=True,
    )
    assert j.decision == "PASS"
    assert j.real_world_side_effects == 0
    assert j.label == "DEMO_PROTOTYPE_NOT_PRODUCTION"


def test_replay_limited_is_not_violation():
    exp = run_replay_experience(mode="limited")
    assert exp["experience"] == "REPLAY_LIMITED"
    assert exp["violation"] is None
    assert exp["replay_status"] == ReplayStatus.REPLAY_LIMITED_BY_ACCESS_CONTEXT.value
    assert "NOT declared false" in exp["message"]


def test_replay_contradiction_blocks():
    exp = run_replay_experience(mode="contradiction")
    assert exp["experience"] == "CONTEXT_MISMATCH"
    assert exp["side_effects"] == 0
    assert exp["recorded_workflow"] == "WF-001"
    assert exp["replay_workflow"] == "WF-002"


def test_replay_tamper_hash_mismatch():
    exp = run_replay_experience(mode="tamper")
    assert exp["experience"] == "HASH_MISMATCH"
    assert exp["side_effects"] == 0


def test_replay_success_bounded():
    exp = run_replay_experience(mode="success")
    assert exp["experience"] == "REPLAYABLE_BOUNDED"
    assert exp["context"] == "MATCH"
