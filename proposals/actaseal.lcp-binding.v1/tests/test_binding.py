from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pytest

from lcp_actaseal_binding import (
    LCP_BINDING_MISMATCH,
    LCP_FINGERPRINT_MISMATCH,
    atr_hash,
    build_lcp_record,
    verify_lcp_record,
)


@dataclass
class FakeReceipt:
    """Minimal stand-in satisfying the PolicyReceipt structural protocol.
    Deliberately not an ActaSeal type -- this package must not import
    ActaSeal internals."""

    decision: str = "ALLOW"
    reason_code: str = "OK"
    action_hash: str = "hash-action-1"
    evidence_set_hash: str = "hash-evidence-1"
    ledger_entry_hash: str = "hash-ledger-1"
    timestamp: str = "2026-07-13T00:00:00Z"
    signature: str = "sig-1"
    mandate_hash: Optional[str] = "hash-mandate-1"


def manifest():
    return {"action_id": "act-123", "scope_conformance_headline": "in-scope"}


def test_atr_hash_is_prefixed_sha256():
    digest = atr_hash(b"terms document bytes")
    assert digest.startswith("0x")
    assert len(digest) == 66


def test_atr_hash_never_invented_only_computed():
    # Same bytes -> same hash, deterministic, no randomness / guessing.
    assert atr_hash(b"abc") == atr_hash(b"abc")
    assert atr_hash(b"abc") != atr_hash(b"abd")


def test_build_lcp_record_with_full_inputs_has_no_unmapped_terms_fields():
    record = build_lcp_record(
        receipt=FakeReceipt(),
        manifest=manifest(),
        terms_url="https://example.com/terms/v3.md",
        terms_document=b"terms",
        terms_format="markdown",
    )
    assert record["legalContext"]["terms"] == "https://example.com/terms/v3.md"
    assert record["legalContext"]["atrHash"] == atr_hash(b"terms")
    assert record["legalContext"]["termsFormat"] == "markdown"
    assert "UNMAPPED:terms" not in record["unmapped"]
    assert "UNMAPPED:atrHash" not in record["unmapped"]
    assert "UNMAPPED:termsFormat" not in record["unmapped"]
    # Fields we truly cannot derive stay explicitly unmapped.
    assert "UNMAPPED:disputeResolution" in record["unmapped"]


def test_build_lcp_record_missing_inputs_are_explicitly_unmapped():
    record = build_lcp_record(receipt=FakeReceipt(), manifest=manifest())
    assert record["legalContext"] == {}
    assert "UNMAPPED:terms" in record["unmapped"]
    assert "UNMAPPED:atrHash" in record["unmapped"]
    assert "UNMAPPED:termsFormat" in record["unmapped"]


def test_build_lcp_record_missing_mandate_is_unmapped():
    receipt = FakeReceipt(mandate_hash=None)
    record = build_lcp_record(receipt=receipt, manifest=manifest())
    assert "UNMAPPED:mandate_hash" in record["unmapped"]


def test_verify_lcp_record_round_trips_clean():
    receipt = FakeReceipt()
    record = build_lcp_record(
        receipt=receipt,
        manifest=manifest(),
        terms_url="https://example.com/terms/v3.md",
        terms_document=b"terms",
    )
    assert verify_lcp_record(record, receipt=receipt, manifest=manifest()) == []


def test_verify_lcp_record_detects_fingerprint_tamper():
    receipt = FakeReceipt()
    record = build_lcp_record(receipt=receipt, manifest=manifest())
    record["record_fingerprint"] = "tampered"
    failures = verify_lcp_record(record, receipt=receipt, manifest=manifest())
    assert any(f.startswith(LCP_FINGERPRINT_MISMATCH) for f in failures)


def test_verify_lcp_record_detects_binding_divergence():
    receipt = FakeReceipt()
    record = build_lcp_record(receipt=receipt, manifest=manifest())
    tampered_receipt = FakeReceipt(decision="BLOCK")
    failures = verify_lcp_record(record, receipt=tampered_receipt, manifest=manifest())
    assert any(f.startswith(f"{LCP_BINDING_MISMATCH}:decision") for f in failures)


def test_no_actaseal_import_anywhere():
    # Package name/docstrings may reference "ActaSeal" as provenance, but
    # no module may *import* anything from the actaseal package.
    import ast
    import pathlib

    src_root = pathlib.Path(__file__).parent.parent / "src" / "lcp_actaseal_binding"
    for path in src_root.glob("*.py"):
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith("actaseal"), path
            if isinstance(node, ast.ImportFrom):
                assert not (node.module or "").startswith("actaseal"), path
