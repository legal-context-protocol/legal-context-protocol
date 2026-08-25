"""Minimal structural interface this package needs from a receipt.

This is intentionally NOT the ActaSeal ``PolicyDecisionReceipt`` class --
this package must not import from, or depend on, the ActaSeal product.
Any object exposing these attributes (dataclass, ORM row, plain
namespace, ...) satisfies this protocol and can be bound to an LCP
record.
"""
from __future__ import annotations

from typing import Optional, Protocol, runtime_checkable


@runtime_checkable
class PolicyReceipt(Protocol):
    """Structural shape of a policy decision receipt, as required for
    LCP terms-fingerprint binding.

    Attributes:
        decision: The policy decision outcome (e.g. "ALLOW", "BLOCK").
        reason_code: Machine-readable reason for the decision.
        action_hash: Hash of the action the decision was made about.
        evidence_set_hash: Hash of the evidence set backing the decision.
        ledger_entry_hash: Hash of the ledger entry recording the decision.
        timestamp: Receipt timestamp.
        signature: Receipt signature.
        mandate_hash: Hash of the governing mandate, if any (None if
            no mandate applies).
    """

    decision: str
    reason_code: str
    action_hash: str
    evidence_set_hash: str
    ledger_entry_hash: str
    timestamp: str
    signature: str
    mandate_hash: Optional[str]
