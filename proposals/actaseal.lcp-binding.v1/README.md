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

# Later, re-derive and check for any divergence:
failures = verify_lcp_record(record, receipt=receipt, manifest=manifest)
assert failures == []  # empty list = verified; every mismatch is named
```

## What this package does NOT do

- It does not fetch `/.well-known/legal-context.json` or any terms
  document over the network.
- It does not define or enforce a receipt/policy schema beyond the
  minimal structural shape it needs (`protocols.PolicyReceipt`).
- It does not implement LCP's dispute-resolution, returns, contact, or
  API discovery fields -- those are surfaced as `UNMAPPED:<field>`
  unless the caller supplies them.

## Development

```
pip install -e '.[test]'
pytest
```

## License

Apache-2.0, matching the [Legal Context Protocol
specification](https://github.com/legal-context-protocol/legal-context-protocol/blob/main/LICENSE).
