"""
SWI Module Kernel — fail-closed pre/post enforcement around one module operation.

WHAT THIS DOES:
  Runs all pre-checks before the operation.
  Runs the operation only if every pre-check passes.
  Runs all post-checks on the output before releasing it.
  Optionally requires a valid AdmissionDecision before formation (universal-gate construction).

WHAT THIS DOES NOT DO:
  This is not CEK, SAD-DFU, Vector Memory, or a global SWI Kernel.
  Default require_admission=False preserves existing callers; Universal Gate is NOT PROVEN
  until Trainer/export and all formation paths set require_admission and supply decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, List, Optional


class ModuleKernelError(RuntimeError):
    """Raised when a module fails its safety contract (pre or post)."""


class AdmissionRequiredError(ModuleKernelError):
    """Raised when require_admission is set and no valid AdmissionDecision is supplied."""


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    reason: str = ""


Check = Callable[[Any], CheckResult]


class ModuleKernel:
    """
    Fail-closed pre/post enforcement around one module operation.

    When require_admission is True, run() refuses to call operation()
    unless a valid AdmissionDecision is provided.
    """

    def __init__(
        self,
        name: str,
        pre_checks: Iterable[Check] = (),
        post_checks: Iterable[Check] = (),
        *,
        require_admission: bool = False,
        module_id: Optional[str] = None,
        expected_commit: Optional[str] = None,
    ) -> None:
        self.name = name
        self.pre_checks = tuple(pre_checks)
        self.post_checks = tuple(post_checks)
        self.require_admission = require_admission
        self.module_id = module_id or name
        self.expected_commit = expected_commit

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

    def run(
        self,
        value: Any,
        operation: Callable[[Any], Any],
        *,
        admission: Any = None,
    ) -> Any:
        # Universal-gate construction: optional choke before formation.
        if self.require_admission:
            if admission is None:
                raise AdmissionRequiredError(
                    f"{self.name}: STATE_FORMATION_WITHOUT_ADMISSION"
                )
            is_valid = getattr(admission, "is_valid_for", None)
            if not callable(is_valid):
                raise AdmissionRequiredError(
                    f"{self.name}: ADMISSION_OBJECT_INVALID"
                )
            if not admission.is_valid_for(
                module=self.module_id,
                commit=self.expected_commit,
            ):
                raise AdmissionRequiredError(
                    f"{self.name}: ADMISSION_NOT_VALID_FOR_CONTEXT"
                )

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
