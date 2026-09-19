"""Formation-path inventory loader and discovery helpers (Security Maze path-closure).

Machine-readable inventory is the source of truth for FM-* identifiers.
Discovery scans source for known patterns and compares to inventory coverage.

Universal Gate remains NOT PROVEN while any privileged path is OPEN/unprotected.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "docs" / "formation_path_inventory.json"

ALLOWED_STATUS = frozenset({"TESTED", "OPEN", "CONSTRUCTION", "TEST_ONLY", "UNKNOWN"})
ALLOWED_CLASS = frozenset(
    {"PRIVILEGED", "CONSTRUCTION_ONLY", "TEST_ONLY", "COMPATIBILITY", "UNKNOWN"}
)

# Source files expected to construct ModuleKernel (production)
EXPECTED_KERNEL_SITES = frozenset(
    {
        "swi_core/module02_security_probe.py",
        "swi_core/module03_context_sync.py",
        "swi_core/module05_redaction_engine.py",
        "swi_core/module06_drift_analyzer.py",
        "swi_core/security_maze.py",
        "swi_core/module_kernel.py",
    }
)

EXPECTED_PUBLIC_APIS = frozenset(
    {
        "Trainer.process",
        "export_foundation_evidence",
        "sign_foundation_evidence",
        "SecurityMaze.evaluate_request",
        "ModuleKernel.run",
        "SecurityProbe.scan",
        "ContextSync.record_turn",
        "RedactionEngine.redact",
        "DriftAnalyzer.check",
    }
)


def load_inventory(path: Path | None = None) -> dict[str, Any]:
    p = path or INVENTORY_PATH
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "paths" not in data:
        raise ValueError("inventory must be an object with paths[]")
    return data


def summarize(inventory: dict[str, Any]) -> dict[str, Any]:
    paths = list(inventory.get("paths") or [])
    def count(pred):
        return sum(1 for x in paths if pred(x))

    privileged_unprotected = count(
        lambda x: x.get("privileged") is True
        and x.get("maze_required") is True
        and x.get("maze_protected") is not True
    )
    return {
        "total_paths": len(paths),
        "unknown_paths": count(lambda x: x.get("status") == "UNKNOWN"),
        "unclassified_paths": count(
            lambda x: x.get("classification") not in ALLOWED_CLASS
            or x.get("classification") == "UNKNOWN"
        ),
        "privileged_paths": count(lambda x: x.get("privileged") is True),
        "maze_protected": count(lambda x: x.get("maze_protected") is True),
        "privileged_unprotected": privileged_unprotected,
        "open_status": count(lambda x: x.get("status") == "OPEN"),
        "tested_status": count(lambda x: x.get("status") == "TESTED"),
        "universal_gate": inventory.get("universal_gate", "NOT_PROVEN"),
    }


def forbidden_closed_records(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    """privileged + maze_required + not protected + status TESTED is illegal as closed."""
    bad = []
    for p in inventory.get("paths") or []:
        if (
            p.get("privileged") is True
            and p.get("maze_required") is True
            and p.get("maze_protected") is not True
            and p.get("status") == "TESTED"
        ):
            bad.append(p)
    return bad


def discover_module_kernel_sites(root: Path | None = None) -> set[str]:
    root = root or ROOT
    sites: set[str] = set()
    for path in (root / "swi_core").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "ModuleKernel(" in text:
            rel = str(path.relative_to(root)).replace("\\", "/")
            sites.add(rel)
    return sites


def discover_public_api_mentions(root: Path | None = None) -> set[str]:
    """Heuristic: presence of known public entry defs in swi_core."""
    root = root or ROOT
    found: set[str] = set()
    patterns = {
        "SecurityProbe.scan": re.compile(r"def scan\("),
        "ContextSync.record_turn": re.compile(r"def record_turn\("),
        "RedactionEngine.redact": re.compile(r"def redact\("),
        "DriftAnalyzer.check": re.compile(r"def check\("),
        "Trainer.process": re.compile(r"def process\("),
        "export_foundation_evidence": re.compile(r"def export_foundation_evidence\("),
        "sign_foundation_evidence": re.compile(r"def sign_foundation_evidence\("),
        "SecurityMaze.evaluate_request": re.compile(r"def evaluate_request\("),
        "ModuleKernel.run": re.compile(r"def run\("),
    }
    core = root / "swi_core"
    for path in core.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for name, rx in patterns.items():
            if rx.search(text):
                # bind to file context roughly
                if name.startswith("SecurityProbe") and "module02" not in path.name:
                    continue
                if name.startswith("ContextSync") and "module03" not in path.name:
                    continue
                if name.startswith("RedactionEngine") and "module05" not in path.name:
                    continue
                if name.startswith("DriftAnalyzer") and "module06" not in path.name:
                    continue
                if name.startswith("Trainer") and "module00" not in path.name:
                    continue
                if name.startswith("SecurityMaze") and "security_maze" not in path.name:
                    continue
                if name.startswith("ModuleKernel") and path.name != "module_kernel.py":
                    continue
                if "foundation" in name and "foundation" not in path.name:
                    continue
                found.add(name)
    return found
