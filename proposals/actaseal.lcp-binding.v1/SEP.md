# SEP: Payment-dispute binding profile: bind atrHash to policy-decision receipts (actaseal.lcp-binding.v1)

## Motivation

LCP v1 deliberately defines no canonical per-transaction receipt schema
(spec/legal-context-protocol-v1.md) and invites the ecosystem to publish
binding profiles for their own receipt shapes. This SEP proposes one such
profile -- registered here as `actaseal.lcp-binding.v1` -- for systems that
produce a receipt-shaped record explaining why an agent's action was
allowed or denied (e.g. a policy gateway sitting in front of agentic
payment actions). It binds LCP's terms fingerprint (`atrHash`) to that
receipt so a payment dispute can be resolved against "what terms were in
force, and were they cryptographically bound to the decision that let the
transaction proceed."

This SEP also proposes, as a secondary and smaller change, that the
specification acknowledge a `proposals/` convention for third-party binding
profiles: at the time of writing there is no established package layout,
namespace, or registration mechanism for binding profiles in this
repository, so this submission had to choose one (a plain top-level
`proposals/<profile-id>/` directory) rather than following an existing
precedent. If the TSC prefers a different convention, this profile's code
will move to match it without any change to its logic.

## Specification

Profile identifier: `actaseal.lcp-binding.v1`.

A binding record is a JSON object:

```json
{
  "lcp_profile": "actaseal.lcp-binding.v1",
  "lcp_spec": "legal-context-protocol v1 (legal-context.schema.json)",
  "legalContext": {
    "terms": "https://example.com/terms/v3.md",
    "atrHash": "0x...sha256 of the terms document bytes...",
    "termsFormat": "markdown"
  },
  "transactionBinding": {
    "action_id": "...",
    "decision": "...",
    "reason_code": "...",
    "action_hash": "...",
    "evidence_set_hash": "...",
    "ledger_entry_hash": "...",
    "receipt_timestamp": "...",
    "receipt_signature": "...",
    "mandate_hash": "...",
    "scope_conformance_headline": "..."
  },
  "unmapped": ["UNMAPPED:disputeResolution", "..."],
  "record_fingerprint": "sha256 hex over the record body, canonical JSON"
}
```

Normative requirements:

- `atrHash` MUST be computed from the actual terms document bytes
  presented to `build_lcp_record` (`0x` + lowercase SHA-256 hex). It MUST
  NOT be accepted from an untrusted party and copied through.
- Every LCP discovery-document field (`spec/legal-context.schema.json`)
  this profile cannot derive from its own inputs (`disputeResolution`,
  `returns`, `contact`, `api`, and `terms`/`atrHash`/`termsFormat` when not
  supplied by the caller) MUST appear in `unmapped` as
  `UNMAPPED:<field>` -- never guessed, never defaulted to a plausible
  value.
- `record_fingerprint` MUST be the canonical-JSON SHA-256 hash of the
  record body (every field except `record_fingerprint` itself).
- Verification (`verify_lcp_record`) MUST re-derive the fingerprint and
  the transaction binding from the presented receipt and manifest, and
  compare -- it MUST NOT trust a stored fingerprint or binding at face
  value. An empty failure list means verified; every mismatch is
  individually named (`LCP_FINGERPRINT_MISMATCH`,
  `LCP_BINDING_MISMATCH:<field>`).
- This profile performs no network I/O. Fetching
  `/.well-known/legal-context.json` and the terms document is the
  caller's responsibility.

Reference implementation: `proposals/actaseal.lcp-binding.v1/` in this PR
-- a dependency-free Python package (`lcp_actaseal_binding`) with no
import on any specific product's receipt type; it only requires a
structural `PolicyReceipt` (decision, reason_code, action_hash,
evidence_set_hash, ledger_entry_hash, timestamp, signature, mandate_hash).

## Backward Compatibility

Purely additive. This profile defines a new record shape and a new
identifier; it does not modify `legal-context.json`, the well-known URI
convention, or the core ATR hashing specification. Existing LCP
implementations are unaffected whether or not they adopt this profile.

## Security Considerations

- `atrHash` binds the *bytes* of the terms document, not a URL or a
  description of it -- a verifier that only checks the URL is not doing
  LCP verification.
- The profile explicitly does not claim coverage of dispute-resolution,
  returns, contact, or API discovery semantics; a verifier relying on
  this profile for those fields would be trusting an `UNMAPPED:` marker,
  which this spec requires to be surfaced, not silently absent.
- `record_fingerprint` covers the whole record body including `unmapped`,
  so a party cannot strip an `UNMAPPED:` marker after the fact without
  invalidating the fingerprint.

## Examples

See `proposals/actaseal.lcp-binding.v1/README.md` for a runnable
build/verify example, and `proposals/actaseal.lcp-binding.v1/tests/test_binding.py`
for round-trip and tamper-detection tests (mutating the receipt or the
record after binding causes verification to fail with a named reason).

## References

- LCP v1 spec: `spec/legal-context-protocol-v1.md`
- LCP discovery schema: `spec/legal-context.schema.json`
- Reference implementation and tests: this PR,
  `proposals/actaseal.lcp-binding.v1/`
- Originally developed for, and in production alongside, ActaSeal (a
  policy gateway for agentic payment actions) -- extracted here as a
  standalone package with zero dependency on that product so it can be
  reviewed and reused independently.
