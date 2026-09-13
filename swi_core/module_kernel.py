"""
SWI Module Kernel — fail-closed pre/post enforcement around one module operation.

WHAT THIS DOES:
  Runs all pre-checks before the operation.
  Runs the operation only if every pre-check passes.
  Runs all post-checks on the output before releasing it.

WHAT THIS DOES NOT DO:
  This is not CEK, SAD-DFU, Vector Memory, or a global SWI Kernel.
  It does not implement module-specific security logic; modules supply checks.
  Advisory (non-halting) checks are not part of this pilot.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, List


class ModuleKernelError(RuntimeError):
    """Raised when a module fails its safety contract (pre or post)."""


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    reason: str = ""


Check = Callable[[Any], CheckResult]


class ModuleKernel:
    """
    Fail-closed pre/post enforcement around one module operation.

    A module is executed only after all pre-checks pass.
    Its output is released only after all post-checks pass.
    """

    def __init__(
        self,
        name: str,
        pre_checks: Iterable[Check] = (),
        post_checks: Iterable[Check] = (),
    ) -> None:
        self.name = name
        self.pre_checks = tuple(pre_checks)
        self.post_checks = tuple(post_checks)

    @staticmethod
    def _run_checks(checks: Iterable[Check], value: Any) -> List[CheckResult]:
        results: List[CheckResult] = []
        for check in checks:
            try:
                result = check(value)
            except Exception as exc:
                raise ModuleKernelError(
                    f"check raised {type(exc).__name__}: {exc}"
                ) from exc
            if not isinstance(result, CheckResult):
                raise ModuleKernelError(
                    f"check {getattr(check, '__name__', check)!r} "
                    "did not return CheckResult"
                )
            results.append(result)
        return results

    def run(self, value: Any, operation: Callable[[Any], Any]) -> Any:
        pre_results = self._run_checks(self.pre_checks, value)
        failed_pre = [r for r in pre_results if not r.passed]
        if failed_pre:
            reasons = "; ".join(f"{r.name}: {r.reason}" for r in failed_pre)
            raise ModuleKernelError(f"{self.name} pre-check failed: {reasons}")

        output = operation(value)

        post_results = self._run_checks(self.post_checks, output)
        failed_post = [r for r in post_results if not r.passed]
        if failed_post:
            reasons = "; ".join(f"{r.name}: {r.reason}" for r in failed_post)
            raise ModuleKernelError(f"{self.name} post-check failed: {reasons}")

        return output
