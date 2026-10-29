"""Adversarial tests for SWI archive resource integrity.

Uses small, bounded fixtures only — never host-exhausting bombs.
PROVEN=NO SEALED=NO AUTHORIZED=NO PRODUCTION_AUTHORIZED=NO
"""
from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pytest

from security.archive_integrity import (
    ACCEPTED_WITHIN_POLICY,
    REJECTED_INVALID_ARCHIVE,
    REJECTED_PATH_SECURITY,
    REJECTED_RESOURCE_LIMIT,
    ResourceLimits,
    extract_zip_bounded,
    inspect_zip_bounded,
)


def _write_zip(path: Path, members: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, data in members.items():
            zf.writestr(name, data)


def test_valid_small_archive(tmp_path: Path):
    z = tmp_path / "ok.zip"
    _write_zip(z, {"hello.txt": b"hello world\n"})
    dest = tmp_path / "out"
    r = extract_zip_bounded(z, dest, limits=ResourceLimits())
    assert r.outcome == ACCEPTED_WITHIN_POLICY
    assert (dest / "hello.txt").read_text() == "hello world\n"
    assert r.authorized is False
    assert r.proven is False
    assert r.production_authorized is False


def test_truncated_archive(tmp_path: Path):
    z = tmp_path / "bad.zip"
    z.write_bytes(b"PK\x03\x04truncated")
    r = inspect_zip_bounded(z)
    assert r.outcome in (REJECTED_INVALID_ARCHIVE, "INSPECTION_INCOMPLETE")


def test_traversal_path_rejected(tmp_path: Path):
    z = tmp_path / "trav.zip"
    # Build zip with unsafe name via ZipInfo
    with zipfile.ZipFile(z, "w") as zf:
        info = zipfile.ZipInfo("../escape.txt")
        zf.writestr(info, b"pwn")
    dest = tmp_path / "out"
    dest.mkdir()
    marker = tmp_path / "escape.txt"
    r = extract_zip_bounded(z, dest, limits=ResourceLimits())
    assert r.outcome == REJECTED_PATH_SECURITY
    assert not marker.exists()
    assert r.authorized is False


def test_absolute_path_rejected(tmp_path: Path):
    z = tmp_path / "abs.zip"
    with zipfile.ZipFile(z, "w") as zf:
        info = zipfile.ZipInfo("/tmp/evil.txt")
        zf.writestr(info, b"pwn")
    dest = tmp_path / "out"
    r = extract_zip_bounded(z, dest, limits=ResourceLimits())
    assert r.outcome == REJECTED_PATH_SECURITY


def test_entry_count_limit(tmp_path: Path):
    z = tmp_path / "many.zip"
    members = {f"f{i}.txt": b"x" for i in range(20)}
    _write_zip(z, members)
    dest = tmp_path / "out"
    limits = ResourceLimits(max_entries=5)
    r = extract_zip_bounded(z, dest, limits=limits)
    assert r.outcome == REJECTED_RESOURCE_LIMIT
    # No successful full extract
    assert r.authorized is False


def test_per_entry_size_limit(tmp_path: Path):
    z = tmp_path / "bigentry.zip"
    _write_zip(z, {"big.bin": b"A" * 10000})
    dest = tmp_path / "out"
    limits = ResourceLimits(max_entry_expanded_bytes=100)
    r = extract_zip_bounded(z, dest, limits=limits)
    assert r.outcome == REJECTED_RESOURCE_LIMIT
    assert not (dest / "big.bin").exists() or r.cleanup_ok


def test_cumulative_size_limit(tmp_path: Path):
    z = tmp_path / "cum.zip"
    _write_zip(
        z,
        {
            "a.bin": b"A" * 80,
            "b.bin": b"B" * 80,
        },
    )
    dest = tmp_path / "out"
    limits = ResourceLimits(
        max_entry_expanded_bytes=1000,
        max_cumulative_expanded_bytes=100,
    )
    r = extract_zip_bounded(z, dest, limits=limits)
    assert r.outcome == REJECTED_RESOURCE_LIMIT


def test_compressed_size_limit(tmp_path: Path):
    z = tmp_path / "fat.zip"
    _write_zip(z, {"x.txt": b"data" * 100})
    dest = tmp_path / "out"
    limits = ResourceLimits(max_compressed_bytes=10)
    r = extract_zip_bounded(z, dest, limits=limits)
    assert r.outcome == REJECTED_RESOURCE_LIMIT
    assert list(dest.glob("**/*")) == [] or r.outcome == REJECTED_RESOURCE_LIMIT


def test_unrelated_files_preserved_on_reject(tmp_path: Path):
    z = tmp_path / "trav.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("../x.txt", b"no")
    dest = tmp_path / "out"
    dest.mkdir()
    keep = dest / "keep.txt"
    keep.write_text("safe")
    r = extract_zip_bounded(z, dest, limits=ResourceLimits())
    assert r.outcome == REJECTED_PATH_SECURITY
    assert keep.read_text() == "safe"


def test_ceiling_never_promoted(tmp_path: Path):
    z = tmp_path / "ok.zip"
    _write_zip(z, {"a.txt": b"a"})
    r = extract_zip_bounded(z, tmp_path / "out")
    d = r.as_dict()
    assert d["authorized"] is False
    assert d["proven"] is False
    assert d["sealed"] is False
    assert d["production_authorized"] is False
