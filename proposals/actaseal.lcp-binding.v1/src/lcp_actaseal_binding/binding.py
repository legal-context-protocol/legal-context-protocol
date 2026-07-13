"""LCP terms-fingerprint binding: the actual profile logic.

Adapted from ActaSeal's internal ``actaseal/adapters/lcp.py`` with zero
behavior change to the fingerprinting/binding/verification logic itself.
The only change from the original is the receipt type: this package
takes a structural ``PolicyReceipt`` (see ``protocols.py``) instead of
importing ActaSeal's concrete ``PolicyDecisionReceipt`` class, so this
package has no dependency on the ActaSeal product.
"""
from __future__ import annotations

import hashlib
from typing import Optional

from ._canonical_json import canonical_json_hash
from .protocols import PolicyReceipt

LCP_PROFILE = "actaseal.lcp-binding.v1"
LCP_SPEC = "legal-context-protocol v1 (legal-context.schema.json)"

LCP_FINGERPRINT_MISMATCH = "LCP_FINGERPRINT_MISMATCH"
LCP_BINDING_MISMATCH = "LCP_BINDING_MISMATCH"

# LCP discovery-document fields (spec/legal-context.schema.json). Only
# `terms` and `atrHash` are derivable from this adapter's inputs; the rest
# require the merchant's actual discovery document and are surfaced as
# UNMAPPED unless supplied.
_LCP_DOCUMENT_FIELDS = (
    "terms",
    "atrHash",
    "termsFormat",
    "acceptanceRequired",
    "disputeResolution",
    "returns",
    "contact",
    "api",
)


def atr_hash(terms_document: bytes) -> str:
    """LCP atrHash: 0x-prefixed lowercase SHA-256 hex of the byte-for-byte
    terms document (the Agentic Transaction Record artifact)."""
    return "0x" + hashlib.sha256(terms_document).hexdigest()


def _binding(receipt: PolicyReceipt, manifest: dict) -> dict:
    return {
        "action_id": manifest["action_id"],
        "decision": receipt.decision,
        "reason_code": receipt.reason_code,
        "action_hash": receipt.action_hash,
        "evidence_set_hash": receipt.evidence_set_hash,
        "ledger_entry_hash": receipt.ledger_entry_hash,
        "receipt_timestamp": receipt.timestamp,
        "receipt_signature": receipt.signature,
        "mandate_hash": receipt.mandate_hash,
        "scope_conformance_headline": manifest["scope_conformance_headline"],
    }


def build_lcp_record(
    *,
    receipt: PolicyReceipt,
    manifest: dict,
    terms_url: Optional[str] = None,
    terms_document: Optional[bytes] = None,
    terms_format: Optional[str] = None,
) -> dict:
    """Map receipt + packet manifest to an LCP binding record: the terms
    fingerprint bound to the transaction. Pure, no network."""
    legal_context: dict = {}
    unmapped: list[str] = []
    if terms_url is not None:
        legal_context["terms"] = terms_url
    else:
        unmapped.append("UNMAPPED:terms")
    if terms_document is not None:
        legal_context["atrHash"] = atr_hash(terms_document)
    else:
        unmapped.append("UNMAPPED:atrHash")
    if terms_format is not None:
        legal_context["termsFormat"] = terms_format
    else:
        unmapped.append("UNMAPPED:termsFormat")
    for field in _LCP_DOCUMENT_FIELDS:
        if field in legal_context or f"UNMAPPED:{field}" in unmapped:
            continue
        unmapped.append(f"UNMAPPED:{field}")

    if receipt.mandate_hash is None:
        unmapped.append("UNMAPPED:mandate_hash")

    record = {
        "lcp_profile": LCP_PROFILE,
        "lcp_spec": LCP_SPEC,
        "legalContext": legal_context,
        "transactionBinding": _binding(receipt, manifest),
        "unmapped": unmapped,
    }
    record["record_fingerprint"] = canonical_json_hash(record)
    return record


def verify_lcp_record(
    record: dict,
    *,
    receipt: PolicyReceipt,
    manifest: dict,
) -> list[str]:
    """Re-derive, never trust: recompute the record fingerprint over the
    record body and re-derive the transaction binding from the presented
    receipt + manifest. Empty list = verified; every divergence is named."""
    failures: list[str] = []

    body = {key: value for key, value in record.items() if key != "record_fingerprint"}
    presented = record.get("record_fingerprint")
    rederived = canonical_json_hash(body)
    if presented != rederived:
        failures.append(
            f"{LCP_FINGERPRINT_MISMATCH}: record carries {presented!r}, "
            f"re-derived {rederived!r}"
        )

    expected_binding = _binding(receipt, manifest)
    recorded_binding = record.get("transactionBinding") or {}
    for field in sorted(set(expected_binding) | set(recorded_binding)):
        if recorded_binding.get(field) != expected_binding.get(field):
            failures.append(
                f"{LCP_BINDING_MISMATCH}:{field}: record has "
                f"{recorded_binding.get(field)!r}, receipt/manifest derive "
                f"{expected_binding.get(field)!r}"
            )
    return failures
