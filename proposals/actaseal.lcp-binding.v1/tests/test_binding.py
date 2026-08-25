from __future__ import annotations

import copy
from dataclasses import dataclass, replace
from typing import Optional

import pytest

from lcp_actaseal_binding import (
    LCP_BINDING_MISMATCH,
    LCP_FINGERPRINT_MISMATCH,
    LCP_RECEIPT_SIGNATURE_INVALID,
    LCP_TERMS_BINDING_UNVERIFIED,
    LCP_TERMS_HASH_MISMATCH,
    atr_hash,
    build_lcp_record,
    verify_lcp_record,
)
from lcp_actaseal_binding._canonical_json import canonical_json_hash


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


def _accept_signature(receipt: FakeReceipt) -> bool:
    """Test double standing in for a real crypto signature check: this
    fixture's receipts are only "genuinely signed" when signature=='sig-1'."""
    return receipt.signature == "sig-1"


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
    assert (
        verify_lcp_record(
            record,
            receipt=receipt,
            manifest=manifest(),
            verify_receipt_signature=_accept_signature,
            terms_document=b"terms",
        )
        == []
    )


def test_verify_lcp_record_detects_fingerprint_tamper():
    receipt = FakeReceipt()
    record = build_lcp_record(receipt=receipt, manifest=manifest())
    record["record_fingerprint"] = "tampered"
    failures = verify_lcp_record(
        record, receipt=receipt, manifest=manifest(), verify_receipt_signature=_accept_signature
    )
    assert any(f.startswith(LCP_FINGERPRINT_MISMATCH) for f in failures)


def test_verify_lcp_record_detects_binding_divergence():
    receipt = FakeReceipt()
    record = build_lcp_record(receipt=receipt, manifest=manifest())
    tampered_receipt = FakeReceipt(decision="BLOCK")
    failures = verify_lcp_record(
        record,
        receipt=tampered_receipt,
        manifest=manifest(),
        verify_receipt_signature=_accept_signature,
    )
    assert any(f.startswith(f"{LCP_BINDING_MISMATCH}:decision") for f in failures)


# --- Regression tests for a hole found by external review (2026-08-26) ---
# The external reviewer reproduced this package as published
# (proposals/actaseal.lcp-binding.v1) and found that verify_lcp_record
# proved only internal consistency, never authenticity: a forged
# receipt.signature, a record built from swapped terms bytes, and a
# hand-tampered atrHash with a recomputed record_fingerprint all
# previously verified with an EMPTY failure list. These three cases are
# the reporter's; landed here so any follow-up contribution from that
# review can drop in alongside them.

FORGED_TERMS_DOC = b"terms (forged)"
REAL_TERMS_DOC = b"terms"


def test_forged_receipt_signature_fails_closed():
    receipt = FakeReceipt(signature="not-a-signature")
    record = build_lcp_record(
        receipt=receipt,
        manifest=manifest(),
        terms_url="https://example.com/terms/v3.md",
        terms_document=REAL_TERMS_DOC,
    )
    failures = verify_lcp_record(
        record,
        receipt=receipt,
        manifest=manifest(),
        verify_receipt_signature=_accept_signature,
        terms_document=REAL_TERMS_DOC,
    )
    assert any(f.startswith(LCP_RECEIPT_SIGNATURE_INVALID) for f in failures)


def test_record_built_from_swapped_terms_bytes_fails_closed():
    receipt = FakeReceipt()
    # same, genuinely-signed receipt; record built over DIFFERENT terms
    # bytes than the ones actually agreed to
    record = build_lcp_record(
        receipt=receipt,
        manifest=manifest(),
        terms_url="https://example.com/terms/v3.md",
        terms_document=FORGED_TERMS_DOC,
    )
    # verifier independently obtains the real terms document
    failures = verify_lcp_record(
        record,
        receipt=receipt,
        manifest=manifest(),
        verify_receipt_signature=_accept_signature,
        terms_document=REAL_TERMS_DOC,
    )
    assert any(f.startswith(LCP_TERMS_HASH_MISMATCH) for f in failures)


def test_tampered_atr_hash_with_recomputed_fingerprint_fails_closed():
    receipt = FakeReceipt()
    record = build_lcp_record(
        receipt=receipt,
        manifest=manifest(),
        terms_url="https://example.com/terms/v3.md",
        terms_document=REAL_TERMS_DOC,
    )
    tampered = copy.deepcopy(record)
    tampered["legalContext"]["atrHash"] = atr_hash(b"a completely different document")
    # attacker recomputes the fingerprint so the internal-consistency
    # check alone would pass
    body = {key: value for key, value in tampered.items() if key != "record_fingerprint"}
    tampered["record_fingerprint"] = canonical_json_hash(body)
    failures = verify_lcp_record(
        tampered,
        receipt=receipt,
        manifest=manifest(),
        verify_receipt_signature=_accept_signature,
        terms_document=REAL_TERMS_DOC,
    )
    assert any(f.startswith(LCP_TERMS_HASH_MISMATCH) for f in failures)


def test_missing_terms_document_is_named_unverified_not_a_pass():
    receipt = FakeReceipt()
    record = build_lcp_record(
        receipt=receipt,
        manifest=manifest(),
        terms_url="https://example.com/terms/v3.md",
        terms_document=REAL_TERMS_DOC,
    )
    failures = verify_lcp_record(
        record, receipt=receipt, manifest=manifest(), verify_receipt_signature=_accept_signature
    )
    assert any(f.startswith(LCP_TERMS_BINDING_UNVERIFIED) for f in failures)


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
