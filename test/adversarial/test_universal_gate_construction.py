"""Universal-gate construction tests.

Proves strict ModuleKernel refuses formation without AdmissionDecision.
Documents that production paths remain ungated (Universal Gate NOT PROVEN).
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from swi_core.admission_boundary import AdmissionDecision, issue_admission_decision
from swi_core.module_kernel import AdmissionRequiredError, ModuleKernel

ROOT = Path(__file__).resolve().parents[2]
SWI_CORE = ROOT / "swi_core"

# Production symbols known to form state without calling admission_boundary.
# Until each is wired, UNIVERSAL_GATE remains NOT_PROVEN.
KNOWN_UNGATED_FORMATION_SYMBOLS = frozenset(
    {
        "Trainer.process",
        "export_foundation_evidence",
        "sign_foundation_evidence",
        "ModuleKernel.run",  # default require_admission=False
    }
)


def test_strict_kernel_rejects_without_admission_formation_never_runs():
    called = {"n": 0}

    def operation(value):
        called["n"] += 1
        return value

    kernel = ModuleKernel(name="strict", require_admission=True, module_id="M05")
    with pytest.raises(AdmissionRequiredError, match="STATE_FORMATION_WITHOUT_ADMISSION"):
        kernel.run("input", operation, admission=None)
    assert called["n"] == 0


def test_strict_kernel_rejects_claim_only_decision():
    called = {"n": 0}

    def operation(value):
        called["n"] += 1
        return value

    decision = issue_admission_decision(
        {"module": "M05", "status": "IMPLEMENTED"},
        grant_execution=False,
    )
    assert decision.execution_authority is False

    kernel = ModuleKernel(
        name="strict",
        require_admission=True,
        module_id="M05",
    )
    with pytest.raises(AdmissionRequiredError):
        kernel.run("input", operation, admission=decision)
    assert called["n"] == 0


def test_strict_kernel_rejects_wrong_module_binding():
    called = {"n": 0}

    def operation(value):
        called["n"] += 1
        return value

    decision = AdmissionDecision(
        ok=True,
        module="M03",
        commit="abcdef0",
        decision="ADMITTED",
        reason="test",
        execution_authority=True,
        architectural_admission=True,
    )
    kernel = ModuleKernel(
        name="strict",
        require_admission=True,
        module_id="M05",
        expected_commit="abcdef0",
    )
    with pytest.raises(AdmissionRequiredError, match="ADMISSION_NOT_VALID_FOR_CONTEXT"):
        kernel.run("input", operation, admission=decision)
    assert called["n"] == 0


def test_strict_kernel_accepts_valid_admission():
    called = {"n": 0}

    def operation(value):
        called["n"] += 1
        return value.upper()

    decision = AdmissionDecision(
        ok=True,
        module="M05",
        commit="abcdef0",
        decision="ADMITTED",
        reason="test",
        execution_authority=True,
        architectural_admission=True,
    )
    kernel = ModuleKernel(
        name="strict",
        require_admission=True,
        module_id="M05",
        expected_commit="abcdef0",
    )
    assert kernel.run("ok", operation, admission=decision) == "OK"
    assert called["n"] == 1


def test_default_kernel_still_runs_without_admission():
    """Document current default: ungated for backward compatibility."""
    called = {"n": 0}

    def operation(value):
        called["n"] += 1
        return value

    kernel = ModuleKernel(name="legacy")  # require_admission=False
    kernel.run("x", operation)
    assert called["n"] == 1


def test_known_ungated_symbols_still_present_in_source():
    """Fail if we claim universal gate while Trainer/export remain free-standing."""
    trainer = (SWI_CORE / "module00_trainer.py").read_text(encoding="utf-8")
    foundation = (SWI_CORE / "foundation_evidence.py").read_text(encoding="utf-8")
    kernel = (SWI_CORE / "module_kernel.py").read_text(encoding="utf-8")

    assert "def process" in trainer
    assert "def export_foundation_evidence" in foundation
    assert "def sign_foundation_evidence" in foundation
    # Default remains False — explicit marker of incomplete universal gate
    assert "require_admission: bool = False" in kernel


def test_admission_boundary_not_imported_by_trainer_or_export():
    """Static: production formation modules must not pretend they gate."""
    for rel in ("module00_trainer.py", "foundation_evidence.py"):
        path = SWI_CORE / rel
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
        assert not any("admission_boundary" in m for m in imports), (
            f"{rel} unexpectedly imports admission_boundary — update UNIVERSAL_GATE status"
        )


def test_universal_gate_status_not_proven():
    """Hard-coded status check — flip only when all paths are wired."""
    status = {
        "universal_gate": "NOT_PROVEN",
        "ungated": sorted(KNOWN_UNGATED_FORMATION_SYMBOLS),
        "strict_kernel_available": True,
    }
    assert status["universal_gate"] == "NOT_PROVEN"
    assert "Trainer.process" in status["ungated"]
