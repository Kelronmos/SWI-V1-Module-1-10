"""
Module 10: External Sandbox (The Air-Gap Shield)

WHAT THIS ACTUALLY DOES:
Runs untrusted Python source code in a separate subprocess with a wall-clock
timeout and, on POSIX systems that provide the resource module, a CPU/memory
resource limit, capturing stdout/stderr and the exit status rather than
executing it inline in the calling process. A runaway or hanging snippet is
killed at the timeout rather than hanging the caller.

WHAT THIS DOES NOT DO:
This is process isolation with resource limits, not a security sandbox
against a determined adversary -- it does not prevent filesystem or network
access from within the subprocess (add OS-level containment such as
containers, seccomp, or a VM for that), and "air-gap" in the marketing sense
of no network path at all is not implemented or verified here.

Portability: the resource module is POSIX-only. On platforms where it is
unavailable, timeout still works; CPU/memory rlimits are simply not applied.
That distinction is intentional and must not be claimed as "full OS isolation."
"""
from __future__ import annotations
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional

try:
    import resource as _resource
except ImportError:  # Windows / non-POSIX
    _resource = None


@dataclass
class SandboxResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool
    resource_limits_applied: bool = False


_LIMIT_PREAMBLE = """
import resource
resource.setrlimit(resource.RLIMIT_CPU, ({cpu}, {cpu}))
resource.setrlimit(resource.RLIMIT_AS, ({mem}, {mem}))
"""


class ExternalSandbox:
    """Module 10: subprocess-isolated execution with timeout and optional resource caps."""

    def __init__(self, timeout_seconds: float = 5.0, cpu_seconds: int = 5, memory_bytes: int = 256 * 1024 * 1024):
        self.timeout_seconds = timeout_seconds
        self.cpu_seconds = cpu_seconds
        self.memory_bytes = memory_bytes

    def run(self, source_code: str) -> SandboxResult:
        apply_limits = _resource is not None
        if apply_limits:
            full_source = _LIMIT_PREAMBLE.format(cpu=self.cpu_seconds, mem=self.memory_bytes) + "\n" + source_code
        else:
            full_source = source_code

        try:
            proc = subprocess.run(
                [sys.executable, "-c", full_source],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )
            return SandboxResult(
                stdout=proc.stdout,
                stderr=proc.stderr,
                exit_code=proc.returncode,
                timed_out=False,
                resource_limits_applied=apply_limits,
            )
        except subprocess.TimeoutExpired as e:
            return SandboxResult(
                stdout=e.stdout or "",
                stderr=(e.stderr or "") + "\n[SANDBOX] timed out",
                exit_code=-1,
                timed_out=True,
                resource_limits_applied=apply_limits,
            )
