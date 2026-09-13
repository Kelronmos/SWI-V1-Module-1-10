"""Shared fail-closed self-check for SWI modules.

Each module should validate its input/operating conditions before processing
and validate its output before passing it to the next module.
"""

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Optional


@dataclass(frozen=True)
class CheckResult:
    passed: bool
    reason: str = ""


class SelfCheck:
    """Run mandatory checks with fail-closed semantics."""

    def __init__(self, checks: Optional[Iterable[Callable[[Any], bool]]] = None):
        self.checks = list(checks or [])

    def validate(self, value: Any) -> CheckResult:
        for check in self.checks:
            try:
                if not bool(check(value)):
                    return CheckResult(False, "mandatory self-check failed")
            except Exception as exc:
                return CheckResult(False, f"self-check error: {type(exc).__name__}")
        return CheckResult(True, "all mandatory self-checks passed")


def require_valid(result: CheckResult) -> None:
    """Raise if a mandatory self-check did not pass."""
    if not result.passed:
        raise ValueError(result.reason)
