"""ActaSeal LCP binding profile.

Legal Context Protocol (LCP) -- co-stewarded by Integra Ledger and the
American Arbitration Association, github.com/legal-context-protocol --
publishes legal terms at /.well-known/legal-context.json and binds a
cryptographic fingerprint of the agreed terms -- ``atrHash``, the
0x-prefixed SHA-256 of the terms document bytes -- to the transaction.
LCP v1 deliberately defines no canonical per-transaction receipt schema;
protocol stewards invite the ecosystem to publish binding profiles. This
package is one such profile: it binds the LCP terms fingerprint to an
ActaSeal-shaped policy decision receipt.

This package has **no** dependency on the ActaSeal product. It depends
only on the minimal ``PolicyReceipt`` protocol defined in
``lcp_actaseal_binding.protocols`` -- any caller can satisfy that shape
with its own receipt type.

Honesty rules (fail-closed, never guess):
- ``atrHash`` is only ever COMPUTED here from the supplied terms document
  bytes; a fingerprint is never accepted on faith or invented.
- Every LCP discovery-document field this adapter cannot honestly derive
  from its inputs is listed as an explicit ``UNMAPPED:<field>`` marker.
- Pure functions, no network: fetching /.well-known/legal-context.json is
  the caller's seam.
"""
from __future__ import annotations

from .binding import (
    LCP_BINDING_MISMATCH,
    LCP_FINGERPRINT_MISMATCH,
    LCP_PROFILE,
    LCP_RECEIPT_SIGNATURE_INVALID,
    LCP_SPEC,
    LCP_TERMS_BINDING_UNVERIFIED,
    LCP_TERMS_HASH_MISMATCH,
    NOT_COVERED,
    atr_hash,
    build_lcp_record,
    verify_lcp_record,
)
from .protocols import PolicyReceipt

__all__ = [
    "LCP_BINDING_MISMATCH",
    "LCP_FINGERPRINT_MISMATCH",
    "LCP_PROFILE",
    "LCP_RECEIPT_SIGNATURE_INVALID",
    "LCP_SPEC",
    "LCP_TERMS_BINDING_UNVERIFIED",
    "LCP_TERMS_HASH_MISMATCH",
    "NOT_COVERED",
    "PolicyReceipt",
    "atr_hash",
    "build_lcp_record",
    "verify_lcp_record",
]
