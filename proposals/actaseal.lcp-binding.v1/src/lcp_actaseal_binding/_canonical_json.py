"""Canonical JSON encoding + hashing, standalone (no ActaSeal dependency).

Deterministic, sorted-key, separator-tight JSON encoding so that the same
logical record always hashes to the same digest regardless of dict
insertion order. Mirrors the encoding used by the ActaSeal product this
binding profile originated in, reimplemented here with zero import from
it.
"""
from __future__ import annotations

import hashlib
import json
from decimal import Decimal


def _canonical_value(value: object) -> object:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _canonical_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_canonical_value(item) for item in value]
    return value


def canonical_json_dumps(value: object) -> str:
    try:
        return json.dumps(
            _canonical_value(value),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except ValueError as exc:
        raise ValueError("canonical JSON does not allow NaN or Infinity") from exc


def canonical_json_hash(value: object) -> str:
    encoded = canonical_json_dumps(value).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
