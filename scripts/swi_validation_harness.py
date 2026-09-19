#!/usr/bin/env python3
"""SWI International Validation Harness (repo-native).

Generates machine-readable evidence from repository identity and declared
control/framework mappings. Does NOT assert legal compliance, certification,
or Universal Gate completeness.

Chain: CLAIM → IMPLEMENTATION → TEST → OBSERVED → HASH → REPORT
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "swi-validation-evidence-v0"

STATUS_VOCAB = [
    "PASS",
    "FAIL",
    "BLOCKED",
    "NOT_TESTED",
    "NOT_PROVEN",
    "PARTIAL",
    "OPEN",
    "PROPOSED",
    "SEALED",
]

HARD_NON_CLAIMS = [
    "Not EU AI Act compliant or certified",
    "Not UN / UNESCO / Council of Europe certified",
    "Not NIST AI RMF certified",
    "Universal Gate is NOT PROVEN",
    "Module 10 is PROPOSED / NOT ADMITTED",
    "Foundation Seal 5 is NOT READY",
    "No automatic compliant conclusion",
    "A green test exercises only the behavior it covers",
]


def _git(*args: str) -> str | None:
    try:
        out = subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _package_meta() -> dict[str, str]:
    name, version = "swi-v1-core", "unknown"
    pyproject = ROOT / "pyproject.toml"
    if pyproject.is_file():
        text = pyproject.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("name = "):
                name = line.split("=", 1)[1].strip().strip('"')
            if line.startswith("version = "):
                version = line.split("=", 1)[1].strip().strip('"')
    return {"name": name, "version": version}


def control_assessments() -> list[dict[str, str]]:
    """Declared from architecture work — not a substitute for live CI."""
    return [
        {
            "control_id": "SWI-ADM-TRAINER",
            "title": "Trainer.process requires AdmissionDecision before formation",
            "status": "PASS",
            "evidence_basis": "Source + adversarial tests (keyword-only admission before _turn_counter)",
            "limitations": "Does not cover direct module APIs",
        },
        {
            "control_id": "SWI-ADM-EXPORT",
            "title": "Foundation export/sign require admission",
            "status": "PASS",
            "evidence_basis": "foundation_evidence.py + tests",
            "limitations": "Depends on suite collection success",
        },
        {
            "control_id": "SWI-ADM-CONTEXT",
            "title": "Module and commit binding on admission",
            "status": "PASS",
            "evidence_basis": "is_valid_for(module, commit) tests",
            "limitations": "Binding strength depends on issuer quality",
        },
        {
            "control_id": "SWI-GATE-UNIVERSAL",
            "title": "Universal Gate over all formation paths",
            "status": "NOT_PROVEN",
            "evidence_basis": "Direct M02–M09 and ModuleKernel default remain ungated",
            "limitations": "Primary residual security gap",
        },
        {
            "control_id": "SWI-KERNEL-DEFAULT",
            "title": "ModuleKernel require_admission default",
            "status": "NOT_PROVEN",
            "evidence_basis": "Default is False (compatibility)",
            "limitations": "Strict mode tested only when enabled",
        },
        {
            "control_id": "SWI-M10",
            "title": "Module 10 BoundaryExporter",
            "status": "PROPOSED",
            "evidence_basis": "Admission status docs",
            "limitations": "Not admitted",
        },
        {
            "control_id": "SWI-SEAL5",
            "title": "Foundation Seal 5",
            "status": "NOT_PROVEN",
            "evidence_basis": "Seal path is experimental; prerequisites incomplete",
            "limitations": "NOT READY",
        },
        {
            "control_id": "SWI-CI-FULL",
            "title": "Full multi-version CI green",
            "status": "NOT_TESTED",
            "evidence_basis": "Re-run required after collection fix tip",
            "limitations": "Do not invent PASS without CI artifact",
        },
    ]


def framework_mappings() -> list[dict[str, str]]:
    """Technical theme alignment only — not legal conformity."""
    return [
        {
            "framework": "EU AI Act",
            "reference": "Art. 9 Risk management",
            "theme": "Lifecycle risk identification and mitigation",
            "swi_surface": "SecurityProbe, DriftAnalyzer, admission, adversarial tests",
            "status": "PARTIAL",
            "notes": "Security gates ≠ documented regulatory risk-management system",
        },
        {
            "framework": "EU AI Act",
            "reference": "Logging / traceability",
            "theme": "Operational event logging",
            "swi_surface": "M07 memory chain, M09 audit log, evidence envelopes",
            "status": "PARTIAL",
            "notes": "Strong direction; full-suite CI and zero-side-effect ∀ paths incomplete",
        },
        {
            "framework": "EU AI Act",
            "reference": "Art. 14 Human oversight",
            "theme": "Effective human oversight",
            "swi_surface": "AdmissionDecision authority binding",
            "status": "PARTIAL",
            "notes": "Architecture promising; responsible human/authority crypto not proven",
        },
        {
            "framework": "EU AI Act",
            "reference": "Robustness / cybersecurity",
            "theme": "Resilience to faults and hostile input",
            "swi_surface": "Adversarial admission suite",
            "status": "PARTIAL",
            "notes": "Gate tests ≠ Universal Gate",
        },
        {
            "framework": "EU AI Act",
            "reference": "Art. 10 Data governance",
            "theme": "Dataset provenance, bias, suitability",
            "swi_surface": "Not established",
            "status": "OPEN",
            "notes": "Future workstream; do not claim via M03/M05/M06",
        },
        {
            "framework": "UN A/RES/78/265",
            "reference": "Safe, secure, trustworthy AI",
            "theme": "Testing, vulnerability identification, lifecycle safeguards",
            "swi_surface": "Admission, evidence, adversarial testing",
            "status": "PARTIAL",
            "notes": "Governance reference, not a technical certification",
        },
        {
            "framework": "UNESCO AI Ethics",
            "reference": "Accountability / oversight / security",
            "theme": "Human rights-aligned AI ethics",
            "swi_surface": "Evidence-first admission model",
            "status": "PARTIAL",
            "notes": "Fairness, non-discrimination, impact assessment OPEN",
        },
        {
            "framework": "Council of Europe AI Convention",
            "reference": "Human rights / democracy / rule of law",
            "theme": "Rights-impact and lifecycle consistency",
            "swi_surface": "Execution integrity (authorized vs should-be-allowed)",
            "status": "OPEN",
            "notes": "SWI answers structural validity more than rights impact",
        },
        {
            "framework": "NIST AI RMF",
            "reference": "Trustworthiness characteristics",
            "theme": "Secure, accountable, transparent",
            "swi_surface": "Admission, audit, claim discipline",
            "status": "PARTIAL",
            "notes": "Voluntary framework; fairness/privacy dimensions OPEN",
        },
    ]


def build_record() -> dict[str, Any]:
    commit = _git("rev-parse", "HEAD") or "UNKNOWN"
    tree = _git("rev-parse", "HEAD^{tree}")
    branch = _git("rev-parse", "--abbrev-ref", "HEAD")
    remote = _git("config", "--get", "remote.origin.url") or (
        "https://github.com/Kelronmos/SWI-V1-Module-1-10"
    )
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "repository": remote,
        "branch": branch,
        "commit": commit,
        "tree": tree,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "package": _package_meta(),
        "status_vocabulary": STATUS_VOCAB,
        "control_assessments": control_assessments(),
        "framework_mappings": framework_mappings(),
        "hard_non_claims": HARD_NON_CLAIMS,
        "invariant": {
            "formation": "∀ production formation paths: formation ⇒ valid AdmissionDecision",
            "rejection": "∀ rejected: formation_count=0 ∧ Δprotected_state=0 ∧ Δunauthorized_side_effects=0",
            "universal_gate": "NOT_PROVEN",
        },
        "chain": [
            "CLAIM",
            "REPOSITORY_IMPLEMENTATION",
            "EXECUTABLE_TEST",
            "OBSERVED_RESULT",
            "CRYPTOGRAPHIC_HASH",
            "REPORT",
        ],
    }
    # Hash without evidence_hash field
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    record["evidence_hash"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return record


def write_csv(path: Path, mappings: list[dict[str, str]]) -> None:
    fields = [
        "framework",
        "reference",
        "theme",
        "swi_surface",
        "status",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in mappings:
            w.writerow({k: row.get(k, "") for k in fields})


def write_markdown(path: Path, record: dict[str, Any]) -> None:
    lines = [
        "# SWI Validation Evidence Report",
        "",
        f"**Generated:** `{record['generated_at']}`  ",
        f"**Commit:** `{record['commit']}`  ",
        f"**Tree:** `{record.get('tree')}`  ",
        f"**Evidence hash:** `{record['evidence_hash']}`  ",
        f"**Package:** `{record['package']['name']}` `{record['package']['version']}`",
        "",
        "> This report is **not** a legal compliance certificate.",
        "",
        "## Hard non-claims",
        "",
    ]
    for c in record["hard_non_claims"]:
        lines.append(f"- {c}")
    lines.extend(["", "## Control assessments", ""])
    lines.append("| ID | Title | Status | Basis |")
    lines.append("|----|-------|--------|-------|")
    for c in record["control_assessments"]:
        lines.append(
            f"| {c['control_id']} | {c['title']} | **{c['status']}** | {c['evidence_basis']} |"
        )
    lines.extend(["", "## Framework theme mappings (technical only)", ""])
    lines.append("| Framework | Reference | Status | Notes |")
    lines.append("|-----------|-----------|--------|-------|")
    for m in record["framework_mappings"]:
        lines.append(
            f"| {m['framework']} | {m['reference']} | **{m['status']}** | {m['notes']} |"
        )
    lines.extend(
        [
            "",
            "## Invariant",
            "",
            f"- Formation: {record['invariant']['formation']}",
            f"- Rejection: {record['invariant']['rejection']}",
            f"- Universal Gate: **{record['invariant']['universal_gate']}**",
            "",
            "**Do not claim what the code cannot demonstrate.**",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "evidence" / "validation",
        help="Output directory for evidence package",
    )
    args = parser.parse_args()
    out: Path = args.out_dir
    out.mkdir(parents=True, exist_ok=True)

    record = build_record()
    json_path = out / "validation_evidence.json"
    csv_path = out / "framework_mapping.csv"
    md_path = out / "VALIDATION_REPORT.md"
    sums_path = out / "SHA256SUMS"

    json_path.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(csv_path, record["framework_mappings"])
    write_markdown(md_path, record)

    lines = []
    for p in (json_path, csv_path, md_path):
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        lines.append(f"{h}  {p.name}")
    sums_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    print(f"Wrote {sums_path}")
    print(f"evidence_hash={record['evidence_hash']}")
    print("UNIVERSAL_GATE=NOT_PROVEN")
    print("NO_COMPLIANCE_CERTIFICATE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
