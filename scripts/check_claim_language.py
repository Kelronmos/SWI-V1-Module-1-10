#!/usr/bin/env python3
"""Flag high-risk claim phrases used as current capability claims."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_AS_CURRENT = [
    "tamper-proof",
    "hardened sandbox",
    "complete isolation",
    "universal prompt injection detection",
    "semantic understanding",
]
SAFE_MARKERS = (
    "not ", "never ", "rather than", "instead of", "without ",
    "does not", "do not", "should not", "must not", "cannot ",
    "can't ", "not claimed", "— not", "- not", "not a ", "not an ",
    "**not**", "no claim", "not:",
)

def _line_is_safe(line: str) -> bool:
    lower = line.lower().strip()
    if any(m in lower for m in SAFE_MARKERS):
        return True
    if lower.startswith("|') and ("not claimed" in lower or "—" in lower):
        return True
    return False

def main() -> None:
    findings = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        if "architecture" in path.parts or "historical" in path.parts:
            continue
        if path.name.startswith("VOLUME_"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for i, line in enumerate(text.splitlines(), 1):
            lower = line.lower()
            for phrase in FORBIDDEN_AS_CURRENT:
                if phrase not in lower:
                    continue
                if _line_is_safe(line):
                    continue
                findings.append(f"{path.relative_to(ROOT)}:{i}: {phrase}")
    if findings:
        print("Documentation claims requiring review:")
        for finding in findings:
            print(f" - {finding}")
        raise SystemExit(1)
    print("Claim-language scan: PASS")

if __name__ == "__main__":
    main()
