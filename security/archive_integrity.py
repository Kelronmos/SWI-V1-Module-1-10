"""SWI bounded archive inspection and extraction.

Enforces Resource Integrity Policy limits while reading/writing.
Does NOT authorize, seal, prove, or grant production rights.

PROVEN=NO SEALED=NO AUTHORIZED=NO PRODUCTION_AUTHORIZED=NO
"""
from __future__ import annotations

import io
import os
import shutil
import stat
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Outcomes (stable)
# ---------------------------------------------------------------------------
ACCEPTED_WITHIN_POLICY = "ACCEPTED_WITHIN_POLICY"
REJECTED_RESOURCE_LIMIT = "REJECTED_RESOURCE_LIMIT"
REJECTED_PATH_SECURITY = "REJECTED_PATH_SECURITY"
REJECTED_INVALID_ARCHIVE = "REJECTED_INVALID_ARCHIVE"
REJECTED_UNSUPPORTED_ENTRY = "REJECTED_UNSUPPORTED_ENTRY"
INSPECTION_INCOMPLETE = "INSPECTION_INCOMPLETE"
PROCESSING_TIMEOUT = "PROCESSING_TIMEOUT"
PROCESSING_FAILED = "PROCESSING_FAILED"


@dataclass
class ResourceLimits:
    max_compressed_bytes: int = 50 * 1024 * 1024
    max_entry_expanded_bytes: int = 25 * 1024 * 1024
    max_cumulative_expanded_bytes: int = 100 * 1024 * 1024
    max_entries: int = 5000
    max_nesting_depth: int = 0  # nested archives not expanded by default
    max_path_length: int = 512
    max_seconds: float = 60.0
    chunk_size: int = 64 * 1024


@dataclass
class ExtractResult:
    outcome: str
    reason: str = ""
    entries_seen: int = 0
    bytes_written: int = 0
    files_written: list[str] = field(default_factory=list)
    cleanup_ok: bool = True
    authorized: bool = False
    proven: bool = False
    sealed: bool = False
    production_authorized: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome,
            "reason": self.reason,
            "entries_seen": self.entries_seen,
            "bytes_written": self.bytes_written,
            "files_written": list(self.files_written),
            "cleanup_ok": self.cleanup_ok,
            "authorized": False,
            "proven": False,
            "sealed": False,
            "production_authorized": False,
            "status": "PASS" if self.outcome == ACCEPTED_WITHIN_POLICY else "FAIL",
        }


def _is_symlink_member(info: zipfile.ZipInfo) -> bool:
    # UNIX external attributes: upper 16 bits are mode
    mode = (info.external_attr >> 16) & 0xFFFF
    return stat.S_ISLNK(mode)


def is_safe_member_name(member_name: str, dest_root: Path, max_path_length: int) -> tuple[bool, str]:
    if not member_name or member_name.strip() == "":
        return False, "empty member name"
    if "\x00" in member_name:
        return False, "null byte in member name"
    if len(member_name) > max_path_length:
        return False, "member name exceeds max path length"
    # Disallow absolute and drive paths
    if member_name.startswith("/") or member_name.startswith("\\"):
        return False, "absolute path"
    if len(member_name) >= 2 and member_name[1] == ":":
        return False, "drive-letter path"
    if member_name.startswith("\\\\") or member_name.startswith("//"):
        return False, "UNC-style path"
    parts = member_name.replace("\\", "/").split("/")
    if any(p == ".." for p in parts):
        return False, "path traversal"
    try:
        root = dest_root.resolve()
        target = (dest_root / member_name).resolve()
        target.relative_to(root)
    except (OSError, ValueError):
        return False, "path escapes extraction root"
    return True, ""


def _cleanup_partial(dest_root: Path, written: list[str]) -> bool:
    ok = True
    # Remove files we wrote, deepest paths first
    for rel in sorted(written, key=lambda s: s.count(os.sep), reverse=True):
        p = dest_root / rel
        try:
            if p.is_file() or p.is_symlink():
                p.unlink(missing_ok=True)
            elif p.is_dir():
                # only remove if empty
                try:
                    p.rmdir()
                except OSError:
                    pass
        except OSError:
            ok = False
    return ok


def inspect_zip_bounded(
    archive_path: Path | str,
    *,
    limits: Optional[ResourceLimits] = None,
) -> ExtractResult:
    """Inspect archive against limits without extracting."""
    limits = limits or ResourceLimits()
    path = Path(archive_path)
    try:
        size = path.stat().st_size
    except OSError as exc:
        return ExtractResult(REJECTED_INVALID_ARCHIVE, f"cannot stat: {exc}")

    if size > limits.max_compressed_bytes:
        return ExtractResult(
            REJECTED_RESOURCE_LIMIT,
            f"compressed size {size} exceeds limit {limits.max_compressed_bytes}",
        )

    try:
        with zipfile.ZipFile(path, "r") as zf:
            names = zf.namelist()
            if len(names) > limits.max_entries:
                return ExtractResult(
                    REJECTED_RESOURCE_LIMIT,
                    f"entry count {len(names)} exceeds limit {limits.max_entries}",
                )
            cumulative = 0
            for info in zf.infolist():
                # Declared size is a signal only; still bound it
                declared = max(0, int(info.file_size))
                if declared > limits.max_entry_expanded_bytes:
                    return ExtractResult(
                        REJECTED_RESOURCE_LIMIT,
                        f"declared entry size exceeds per-entry limit: {info.filename}",
                    )
                cumulative += declared
                if cumulative > limits.max_cumulative_expanded_bytes:
                    return ExtractResult(
                        REJECTED_RESOURCE_LIMIT,
                        "declared cumulative size exceeds limit",
                    )
            return ExtractResult(
                ACCEPTED_WITHIN_POLICY,
                "inspection within declared bounds (extract still enforces actual bytes)",
                entries_seen=len(names),
            )
    except zipfile.BadZipFile:
        return ExtractResult(REJECTED_INVALID_ARCHIVE, "bad zip file")
    except OSError as exc:
        return ExtractResult(INSPECTION_INCOMPLETE, f"os error: {exc}")


def extract_zip_bounded(
    archive_path: Path | str,
    dest_root: Path | str,
    *,
    limits: Optional[ResourceLimits] = None,
    allow_symlinks: bool = False,
) -> ExtractResult:
    """Extract ZIP under resource and path policy.

    Never calls ZipFile.extractall(). Writes entry-by-entry with running totals.
    """
    limits = limits or ResourceLimits()
    archive_path = Path(archive_path)
    dest_root = Path(dest_root)
    start = time.monotonic()
    written: list[str] = []
    bytes_written = 0
    entries_seen = 0

    def timed_out() -> bool:
        return (time.monotonic() - start) > limits.max_seconds

    try:
        compressed_size = archive_path.stat().st_size
    except OSError as exc:
        return ExtractResult(REJECTED_INVALID_ARCHIVE, f"cannot stat: {exc}")

    if compressed_size > limits.max_compressed_bytes:
        return ExtractResult(
            REJECTED_RESOURCE_LIMIT,
            f"compressed size {compressed_size} exceeds limit",
        )

    try:
        dest_root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return ExtractResult(PROCESSING_FAILED, f"cannot create dest: {exc}")

    try:
        zf = zipfile.ZipFile(archive_path, "r")
    except zipfile.BadZipFile:
        return ExtractResult(REJECTED_INVALID_ARCHIVE, "bad zip file")
    except OSError as exc:
        return ExtractResult(INSPECTION_INCOMPLETE, f"os error: {exc}")

    try:
        infos = zf.infolist()
        if len(infos) > limits.max_entries:
            return ExtractResult(
                REJECTED_RESOURCE_LIMIT,
                f"entry count {len(infos)} exceeds limit",
            )

        for info in infos:
            if timed_out():
                cleanup_ok = _cleanup_partial(dest_root, written)
                return ExtractResult(
                    PROCESSING_TIMEOUT,
                    "processing time exceeded",
                    entries_seen=entries_seen,
                    bytes_written=bytes_written,
                    files_written=written,
                    cleanup_ok=cleanup_ok,
                )

            entries_seen += 1
            name = info.filename

            ok, why = is_safe_member_name(name, dest_root, limits.max_path_length)
            if not ok:
                cleanup_ok = _cleanup_partial(dest_root, written)
                return ExtractResult(
                    REJECTED_PATH_SECURITY,
                    why,
                    entries_seen=entries_seen,
                    bytes_written=bytes_written,
                    files_written=written,
                    cleanup_ok=cleanup_ok,
                )

            if _is_symlink_member(info) and not allow_symlinks:
                cleanup_ok = _cleanup_partial(dest_root, written)
                return ExtractResult(
                    REJECTED_UNSUPPORTED_ENTRY,
                    f"symlink not allowed: {name}",
                    entries_seen=entries_seen,
                    bytes_written=bytes_written,
                    files_written=written,
                    cleanup_ok=cleanup_ok,
                )

            # Nested archive marker: if nesting disallowed, still allow storing
            # the compressed member as a normal file, but do not recursively expand.
            # (Recursive expansion is not implemented; max_nesting_depth=0 means no recurse.)

            target = dest_root / name
            if name.endswith("/") or info.is_dir():
                try:
                    target.mkdir(parents=True, exist_ok=True)
                    written.append(name.rstrip("/"))
                except OSError as exc:
                    cleanup_ok = _cleanup_partial(dest_root, written)
                    return ExtractResult(
                        PROCESSING_FAILED,
                        f"mkdir failed: {exc}",
                        entries_seen=entries_seen,
                        bytes_written=bytes_written,
                        files_written=written,
                        cleanup_ok=cleanup_ok,
                    )
                continue

            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                entry_bytes = 0
                with zf.open(info, "r") as src, open(target, "wb") as dst:
                    while True:
                        if timed_out():
                            dst.close()
                            cleanup_ok = _cleanup_partial(dest_root, written + [name])
                            return ExtractResult(
                                PROCESSING_TIMEOUT,
                                "processing time exceeded during write",
                                entries_seen=entries_seen,
                                bytes_written=bytes_written + entry_bytes,
                                files_written=written,
                                cleanup_ok=cleanup_ok,
                            )
                        chunk = src.read(limits.chunk_size)
                        if not chunk:
                            break
                        entry_bytes += len(chunk)
                        if entry_bytes > limits.max_entry_expanded_bytes:
                            dst.close()
                            cleanup_ok = _cleanup_partial(dest_root, written + [name])
                            return ExtractResult(
                                REJECTED_RESOURCE_LIMIT,
                                f"per-entry expanded size exceeded: {name}",
                                entries_seen=entries_seen,
                                bytes_written=bytes_written + entry_bytes,
                                files_written=written,
                                cleanup_ok=cleanup_ok,
                            )
                        if bytes_written + entry_bytes > limits.max_cumulative_expanded_bytes:
                            dst.close()
                            cleanup_ok = _cleanup_partial(dest_root, written + [name])
                            return ExtractResult(
                                REJECTED_RESOURCE_LIMIT,
                                "cumulative expanded size exceeded",
                                entries_seen=entries_seen,
                                bytes_written=bytes_written + entry_bytes,
                                files_written=written,
                                cleanup_ok=cleanup_ok,
                            )
                        dst.write(chunk)
                bytes_written += entry_bytes
                written.append(name)
            except OSError as exc:
                cleanup_ok = _cleanup_partial(dest_root, written + [name])
                return ExtractResult(
                    PROCESSING_FAILED,
                    f"write failed: {exc}",
                    entries_seen=entries_seen,
                    bytes_written=bytes_written,
                    files_written=written,
                    cleanup_ok=cleanup_ok,
                )

        return ExtractResult(
            ACCEPTED_WITHIN_POLICY,
            "extracted within policy",
            entries_seen=entries_seen,
            bytes_written=bytes_written,
            files_written=written,
            cleanup_ok=True,
        )
    finally:
        try:
            zf.close()
        except Exception:
            pass
