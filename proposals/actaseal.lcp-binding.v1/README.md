# lcp-actaseal-binding

A [Legal Context Protocol (LCP)](https://github.com/legal-context-protocol/legal-context-protocol)
binding profile: it binds the LCP terms fingerprint (`atrHash`) to a
policy decision receipt, for agentic commerce systems that produce a
receipt-shaped record of "why an agent's action was allowed."

LCP v1 deliberately defines no canonical per-transaction receipt schema
(see the [spec](https://github.com/legal-context-protocol/legal-context-protocol/blob/main/spec/legal-context-protocol-v1.md));
protocol stewards invite the ecosystem to publish binding profiles for
their own receipt shapes. This is one such profile, originally written
for [ActaSeal](https://github.com/legal-context-protocol/legal-context-protocol)
and extracted here as a standalone, dependency-free package so it can be
reused (and reviewed) independent of any one product.

**This package has no dependency on ActaSeal, or any other specific
policy/receipt system.** It only requires an object matching the
structural `PolicyReceipt` protocol below.

## Why this profile

- `atrHash` is only ever **computed** here from terms document bytes you
  supply -- never accepted on faith, never invented.
- Every LCP discovery-document field this profile cannot honestly derive
  from its inputs is listed as an explicit `UNMAPPED:<field>` marker, so
  a verifier can see exactly what was, and wasn't, checked.
- Pure functions, no network I/O: fetching
  `/.well-known/legal-context.json` and the terms document itself is the
  caller's responsibility (the "seam").
- Verification re-derives everything from the presented receipt and
  manifest -- it never trusts a stored fingerprint or binding at face
  value.

## Install

```
pip install lcp-actaseal-binding
```

## Usage

```python
from lcp_actaseal_binding import build_lcp_record, verify_lcp_record

# `receipt` is any object with: decision, reason_code, action_hash,
# evidence_set_hash, ledger_entry_hash, timestamp, signature,
# mandate_hash (see PolicyReceipt in protocols.py).
record = build_lcp_record(
    receipt=receipt,
    manifest={"action_id": "act-123", "scope_conformance_headline": "in-scope"},
    terms_url="https://example.com/terms/v3.md",
    terms_document=terms_bytes,
    terms_format="markdown",
)

# Later, re-derive and check for any divergence. verify_receipt_signature
# is YOUR receipt system's own real signature check -- this package has
# no crypto dependency of its own and never re-implements one; it must
# be given the same verification path your system already trusts (in
# ActaSeal's case, actaseal.receipt.verify_receipt). terms_document is
# the real terms bytes, independently obtained (e.g. by fetching
# legalContext.terms yourself) -- never trust a document the record
# merely claims to be bound to.
failures = verify_lcp_record(
    record,
    receipt=receipt,
    manifest=manifest,
    verify_receipt_signature=lambda r: my_verify_receipt_signature(r, public_key),
    terms_document=terms_bytes,
)
assert failures == []  # empty list = verified; every mismatch -- or unchecked gap -- is named
```

Omitting `terms_document` from `verify_lcp_record` does not mean "pass": if the record claims an `atrHash`, verification returns a named
`LCP_TERMS_BINDING_UNVERIFIED` entry instead of an empty list, so silence and pass never look alike.

## What this package does NOT do

- It does not fetch `/.well-known/legal-context.json` or any terms
  document over the network.
- It does not define or enforce a receipt/policy schema beyond the
  minimal structural shape it needs (`protocols.PolicyReceipt`).
- It does not implement LCP's dispute-resolution, returns, contact, or
  API discovery fields -- those are surfaced as `UNMAPPED:<field>`
  unless the caller supplies them (as plain metadata, e.g. a URL or
  contact string -- see the `atrHash` note below for the one field this
  does NOT apply to).

`atrHash` is the one exception to "the caller can supply a field to
avoid UNMAPPED": it is **only ever computed** by this profile from
`terms_document` bytes you supply, never accepted pre-computed. A
caller-supplied `atr_hash=` passthrough is not a conformant variant of
this profile and will not be added -- LCP's own spec requires that
`atrHash` "MUST NOT be accepted from an untrusted party and copied
through", and a hash accepted on faith from the caller is exactly that.
There is deliberately no third code path here beyond "computed from
bytes" or "UNMAPPED"; if that reads as looser in older prose or in
other implementers' summaries of this profile, this paragraph is the
normative correction. (A record produced by this profile also does not
carry a field recording *how* its `atrHash` was obtained -- a verifier
trusts the profile implementation itself to enforce this rule, the same
way it trusts any other library not to lie about what it computed.
Adding such a provenance field was considered and rejected for this
pass: it would only push the trust question down one level, since a
non-conformant fork could set `"atrHash_provenance": "computed"` just
as easily as it could add a passthrough parameter -- provenance in the
record does not substitute for a downstream verifier pinning which
profile *implementation*, not just which profile *name*, it trusts.)

## Development

```
pip install -e '.[test]'
pytest
```

## License

Apache-2.0, matching the [Legal Context Protocol
specification](https://github.com/legal-context-protocol/legal-context-protocol/blob/main/LICENSE).
