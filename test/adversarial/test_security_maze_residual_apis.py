"""Path-closure campaign — residual public APIs.

These tests DOCUMENT current production behavior:
  scan / record_turn / redact / check run without AdmissionDecision.

They are NOT a claim that this is acceptable as Universal Gate.
When a residual is closed, flip the corresponding assertion and
update docs/SECURITY_MAZE_RESIDUAL_PATHS.md.

Classification: PRODUCTION residual (ModuleKernel default require_admission=False).
"""
from __future__ import annotations

from swi_core.module02_security_probe import SecurityProbe
from swi_core.module03_context_sync import ContextSync
from swi_core.module05_redaction_engine import RedactionEngine
from swi_core.module06_drift_analyzer import DriftAnalyzer


def test_residual_security_probe_scan_without_admission():
    """ATTACK residual: SecurityProbe.scan forms ProbeResult without admission."""
    probe = SecurityProbe()
    assert probe.kernel.require_admission is False
    result = probe.scan("hello world")
    assert result is not None
    assert hasattr(result, "risk_score")


def test_residual_context_sync_record_turn_without_admission():
    """ATTACK residual: ContextSync.record_turn mutates history without admission."""
    sync = ContextSync()
    assert sync.kernel.require_admission is False
    result = sync.record_turn(1)
    assert result is not None
    assert len(sync.history()) == 1


def test_residual_redaction_engine_redact_without_admission():
    """ATTACK residual: RedactionEngine.redact forms output without admission."""
    engine = RedactionEngine()
    assert engine.kernel.require_admission is False
    out = engine.redact("contact me at test@example.com")
    assert out is not None


def test_residual_drift_analyzer_check_without_admission():
    """ATTACK residual: DriftAnalyzer.check forms result without admission."""
    analyzer = DriftAnalyzer()
    assert analyzer.kernel.require_admission is False
    # check signature: use a minimal valid call if possible
    result = analyzer.check({"baseline": "a", "observed": "a"})
    assert result is not None


def test_residual_module_kernels_default_false_inventory():
    """Inventory: sealed-module public classes still default ungated."""
    inventory = {
        "SecurityProbe": SecurityProbe().kernel.require_admission,
        "ContextSync": ContextSync().kernel.require_admission,
        "RedactionEngine": RedactionEngine().kernel.require_admission,
        "DriftAnalyzer": DriftAnalyzer().kernel.require_admission,
    }
    assert all(v is False for v in inventory.values()), inventory
    # Marker for Universal Gate status
    assert inventory  # non-empty residual set ⇒ NOT PROVEN
