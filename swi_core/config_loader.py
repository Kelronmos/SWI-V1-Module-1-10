"""
Shared Config Loader (Module 00 dependency)

WHAT THIS ACTUALLY DOES:
Loads a YAML config file into a plain dict, applies documented defaults
for any missing keys, and optionally overrides values from environment
variables using a documented naming convention (SWI_<SECTION>_<KEY>).
Raises on malformed YAML rather than silently ignoring it.

`Trainer` (module00_trainer.py) calls this to configure the
SecurityProbe block_threshold and ContextSync staleness_seconds it
constructs. No other module in this package reads it directly --
Modules 01/04/08/10 are still configured only via constructor
arguments when used standalone.

WHAT THIS DOES NOT DO:
It does not watch the file for changes, does not support multiple
config files merged together, and does not validate values against
each module's actual accepted ranges (e.g. it will happily load
block_threshold: 5.0 even though SecurityProbe expects roughly 0-1;
range validation is left to the caller for now).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import yaml

DEFAULTS: Dict[str, Dict[str, Any]] = {
    "security_probe": {"block_threshold": 0.5},
    "context_sync": {"staleness_seconds": 1800.0},
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
        """Convenience accessor: get('security_probe', 'block_threshold')."""
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


def load_config(path: Optional[str] = None, apply_env: bool = True) -> ConfigLoadResult:
    """
    Load config from `path` if given and it exists, else use defaults only.
    Missing keys within a present section are filled from DEFAULTS.
    Unknown sections in the file are ignored (not merged, not erroring) --
    only sections named in DEFAULTS are recognized.
    """
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

    return ConfigLoadResult(
        values=merged,
        source_path=path if (path and os.path.exists(path)) else None,
        env_overrides_applied=applied,
    )
