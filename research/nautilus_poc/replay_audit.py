"""Versioned canonical JSON and SHA-256 helpers for isolated replay audits.

This is research-only POC code, not the IDEAL runtime serializer.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any


SCHEMA = "ideal-replay-audit/v1"


def _validate(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        raise TypeError(f"floating-point values are not canonical at {path}; encode exact decimals as strings")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate(item, f"{path}/{index}")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError(f"canonical object key must be a string at {path}")
            _validate(item, f"{path}/{key}")
        return
    raise TypeError(f"unsupported canonical value {type(value).__name__} at {path}")


def canonical_bytes(snapshot: dict[str, Any]) -> bytes:
    """Return deterministic compact UTF-8 JSON; Decimal values must be strings."""
    if not isinstance(snapshot, dict):
        raise TypeError("snapshot must be a dictionary")
    if snapshot.get("schema") != SCHEMA:
        raise ValueError(f"snapshot schema must be {SCHEMA!r}")
    _validate(snapshot)
    return json.dumps(
        snapshot,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_digest(snapshot: dict[str, Any]) -> str:
    """Return a versioned SHA-256 digest for a canonical replay snapshot."""
    return "sha256:" + hashlib.sha256(canonical_bytes(snapshot)).hexdigest()
