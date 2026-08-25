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
from typing import Callable, Optional

from ._canonical_json import canonical_json_hash
from .protocols import PolicyReceipt

LCP_PROFILE = "actaseal.lcp-binding.v1"
LCP_SPEC = "legal-context-protocol v1 (legal-context.schema.json)"

LCP_FINGERPRINT_MISMATCH = "LCP_FINGERPRINT_MISMATCH"
LCP_BINDING_MISMATCH = "LCP_BINDING_MISMATCH"
# Reported by external review (2026-08-26): the two checks above only
# ever prove *internal* consistency -- never authenticity. A forged
# receipt.signature, a record built from swapped terms bytes, or a
# hand-tampered atrHash with a recomputed record_fingerprint all
# previously verified clean. Closed by the two checks below.
LCP_RECEIPT_SIGNATURE_INVALID = "LCP_RECEIPT_SIGNATURE_INVALID"
LCP_TERMS_HASH_MISMATCH = "LCP_TERMS_HASH_MISMATCH"
# Not a mismatch -- an explicit "not checked" state (same discipline as
# ConformanceResult.unconstrained in the ActaSeal product this profile
# originated from): a caller that omits terms_document gets this named
# marker instead of a silent, indistinguishable pass.
LCP_TERMS_BINDING_UNVERIFIED = "LCP_TERMS_BINDING_UNVERIFIED"

# Design gaps this profile does not close, stated rather than hidden.
# Out of scope for this pass per external review 2026-08-26: these are
# design questions about what a bound mandate/scope claim actually
# proves, not bugs in the terms-fingerprint authentication this pass
# fixed.
NOT_COVERED = (
    "mandate_hash proves a mandate was BOUND to this transaction, not "
    "what it authorized, who granted it, whether it had expired, or "
    "whether this action fell inside its scope.",
    "scope_conformance_headline is free text supplied by the manifest "
    "producer: it ASSERTS conformance, it does not EVIDENCE it. A "
    "verifier must not treat this field as proof of in-scope action.",
)

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
        "not_covered": list(NOT_COVERED),
    }
    record["record_fingerprint"] = canonical_json_hash(record)
    return record


def verify_lcp_record(
    record: dict,
    *,
    receipt: PolicyReceipt,
    manifest: dict,
    verify_receipt_signature: Callable[[PolicyReceipt], bool],
    terms_document: Optional[bytes] = None,
) -> list[str]:
    """Re-derive, never trust: recompute the record fingerprint over the
    record body, re-derive the transaction binding from the presented
    receipt + manifest, cryptographically verify the receipt signature
    itself, and (when terms_document is supplied) re-hash the real terms
    bytes against the record's claimed atrHash. Empty list = verified;
    every divergence -- or unchecked gap -- is named.

    Internal consistency (fingerprint/binding re-derivation) alone proves
    a record is self-consistent, never that it was authentic: a forged
    receipt.signature, or a record built over swapped/tampered terms
    bytes, can be made perfectly self-consistent.

    verify_receipt_signature is a caller-supplied predicate that takes
    `receipt` and returns whether its signature cryptographically
    verifies. This package is deliberately dependency-free and
    receipt-type-agnostic (PolicyReceipt is a *structural* protocol, not
    a concrete class), so it cannot embed a signature-verification stack
    of its own without either adding a hard crypto dependency or hard-
    coding one algorithm -- that would make it a SECOND, divergent
    signature check next to whatever real implementation the caller's
    receipt system already has (in ActaSeal's own case,
    actaseal.receipt.verify_receipt, the same path
    actaseal/dispute/offline_verifier.py's verify_receipt() uses).
    Dependency injection here means callers always reuse their own one
    true signature-verification path; this package never re-implements
    it.

    The claimed atrHash is authenticated by re-hashing terms_document --
    ground truth the caller must independently obtain (e.g. by fetching
    legalContext.terms) -- rather than trusted from the record body.
    """
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

    if not verify_receipt_signature(receipt):
        failures.append(
            f"{LCP_RECEIPT_SIGNATURE_INVALID}: receipt signature does not "
            f"cryptographically verify"
        )

    claimed_atr_hash = (record.get("legalContext") or {}).get("atrHash")
    if claimed_atr_hash is not None:
        if terms_document is not None:
            recomputed = atr_hash(terms_document)
            if claimed_atr_hash != recomputed:
                failures.append(
                    f"{LCP_TERMS_HASH_MISMATCH}: record claims atrHash "
                    f"{claimed_atr_hash!r}, the presented terms_document "
                    f"bytes hash to {recomputed!r}"
                )
        else:
            failures.append(
                f"{LCP_TERMS_BINDING_UNVERIFIED}: record claims atrHash "
                f"{claimed_atr_hash!r} but no terms_document bytes were "
                f"presented to verify_lcp_record, so the terms binding "
                f"was not checked -- this is NOT a pass"
            )
    return failures
