"""
Shared configuration loader for SWI Modules 00-10.

Runtime-wired Trainer settings (validated):
  - security_probe.block_threshold  (finite, 0.0–1.0)
  - context_sync.staleness_seconds  (finite, >= 0)
  - drift_analyzer.drift_threshold  (finite, 0.0–1.0)

Other YAML sections may exist as documentation/reference only until wired.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import yaml

DEFAULTS: Dict[str, Dict[str, Any]] = {
    "security_probe": {"block_threshold": 0.5},
    "context_sync": {"staleness_seconds": 1800.0},
    "drift_analyzer": {"drift_threshold": 0.35},
    "encryption": {"key_length_bytes": 32},
    "access_auth": {"token_ttl_seconds": 3600.0},
    "sandbox": {
        "timeout_seconds": 5.0,
        "cpu_seconds": 5,
        "memory_bytes": 256 * 1024 * 1024,
    },
}


@dataclass
class ConfigLoadResult:
    values: Dict[str, Dict[str, Any]]
    source_path: Optional[str]
    env_overrides_applied: List[str] = field(default_factory=list)

    def get(self, section: str, key: str) -> Any:
        return self.values[section][key]


class ConfigError(Exception):
    """Raised when the config file exists but cannot be parsed as expected."""


def _deep_merge_defaults(loaded: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    merged: Dict[str, Dict[str, Any]] = {}
    for section, section_defaults in DEFAULTS.items():
        loaded_section = loaded.get(section, {}) if isinstance(loaded, dict) else {}
        if not isinstance(loaded_section, dict):
            raise ConfigError(
                f"Section '{section}' must be a mapping, got {type(loaded_section).__name__}"
            )
        merged[section] = {**section_defaults, **loaded_section}
    return merged


def _apply_env_overrides(values: Dict[str, Dict[str, Any]]) -> List[str]:
    applied: List[str] = []
    for section, keys in values.items():
        for key, current in keys.items():
            env_name = f"SWI_{section.upper()}_{key.upper()}"
            if env_name in os.environ:
                raw = os.environ[env_name]
                cast = type(current) if current is not None else str
                try:
                    values[section][key] = cast(raw)
                except (TypeError, ValueError) as exc:
                    raise ConfigError(
                        f"Environment variable {env_name}={raw!r} could not be "
                        f"cast to {cast.__name__}: {exc}"
                    ) from exc
                applied.append(env_name)
    return applied


def _require_finite_number(section: str, key: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError(
            f"{section}.{key} must be numeric, got {type(value).__name__}"
        )
    fv = float(value)
    if not math.isfinite(fv):
        raise ConfigError(f"{section}.{key} must be finite, got {value!r}")
    return fv


def _validate_runtime_values(values: Dict[str, Dict[str, Any]]) -> None:
    bt = _require_finite_number(
        "security_probe", "block_threshold", values["security_probe"]["block_threshold"]
    )
    if bt < 0.0 or bt > 1.0:
        raise ConfigError(
            f"security_probe.block_threshold must be in [0.0, 1.0], got {bt}"
        )
    values["security_probe"]["block_threshold"] = bt

    ss = _require_finite_number(
        "context_sync",
        "staleness_seconds",
        values["context_sync"]["staleness_seconds"],
    )
    if ss < 0.0:
        raise ConfigError(
            f"context_sync.staleness_seconds must be >= 0, got {ss}"
        )
    values["context_sync"]["staleness_seconds"] = ss

    dt = _require_finite_number(
        "drift_analyzer",
        "drift_threshold",
        values["drift_analyzer"]["drift_threshold"],
    )
    if dt < 0.0 or dt > 1.0:
        raise ConfigError(
            f"drift_analyzer.drift_threshold must be in [0.0, 1.0], got {dt}"
        )
    values["drift_analyzer"]["drift_threshold"] = dt


def load_config(path: Optional[str] = None, apply_env: bool = True) -> ConfigLoadResult:
    loaded: Dict[str, Any] = {}
    if path is not None and os.path.exists(path):
        with open(path, "r") as f:
            try:
                loaded = yaml.safe_load(f) or {}
            except yaml.YAMLError as exc:
                raise ConfigError(f"Malformed YAML in {path}: {exc}") from exc
        if not isinstance(loaded, dict):
            raise ConfigError(f"{path} must parse to a mapping at the top level")

    merged = _deep_merge_defaults(loaded)
    applied = _apply_env_overrides(merged) if apply_env else []
    _validate_runtime_values(merged)

    return ConfigLoadResult(
        values=merged,
        source_path=path if (path and os.path.exists(path)) else None,
        env_overrides_applied=applied,
    )
