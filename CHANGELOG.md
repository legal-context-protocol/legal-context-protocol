# Changelog

All notable changes to the Legal Context Protocol are recorded here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The
specification edition is carried in the document header; repository releases are
tagged to match.

## [Unreleased]

### Fixed

Corrections to the published 1.0 text. Each removes or repairs a statement that
is not true; no field is added, removed or renamed.

- **§11 IANA Considerations** stated Status "Provisional" and cited
  `/.well-known/ucp` as a registered neighbour. Neither `legal-context.json`
  nor `ucp` is in the IANA Well-Known URIs registry. The table now states the
  registration sought rather than one granted. `FAQ.md` made the stronger
  claim — "IANA-registered well-known URI" — and is corrected too.
- **§E.4** held that `disputeResolution.method` and `.jurisdiction`, "when
  accepted by both parties (Level 3), constitute mutual selection of forum and
  governing law". Level 3 signs `atrHash`, which fixes the terms document and
  nothing else; nothing in Level 3 accepts the discovery document. A deployment
  that read this and published its forum only in `legal-context.json` would
  hold a signed record containing no selection at all. §E.4 also claimed
  `clauseId` eliminates disputes about which clause version applied, and called
  the `api` / `returns` / `contact.legal` fields "binding".
- **Appendix C** carried placements the host protocols reject: Verifiable
  Intent as Tier A (verifiers MUST reject open mandates with unknown constraint
  types, and Immediate-mode credentials carry no `constraints` array); an AP2
  open Checkout Mandate constraint (the array is a closed `anyOf`); a UCP
  `extensions` map that does not exist on the checkout response; Visa TAP's
  `kid` where [RFC 9421] says `keyid`; an MPP challenge MAC described as
  committing the seller, when it uses a server-held secret and commits nobody
  without the key; and eight MPP charge methods where there are ten, under a
  core draft that is an individual submission not endorsed by the IETF. x402's
  extension-echo rule is stated in lower case and about the `info` payload
  rather than the map. Appendix D marked Verifiable Intent as providing no
  agent identity.
- **§C.1 and §C.4** paired a per-transaction `atrHash` with the discovery
  document's own URL — bytes that can never hash to the value beside them.
- **`examples/level-4-full.json`** failed the schema it ships beside:
  `disputeResolution.source` and `.catalog` carried brace placeholders that are
  not valid URIs.
- **`spec/legal-context.schema.json`** `$id` named `www.legalcontextprotocol.org`,
  which redirects, and disagreed with the copy the website serves.
- **§13** cited the Model Context Protocol at spec version 2025-11-25 with a
  2026-07-28 revision "in Release Candidate". That revision is final.

### Changed

- **The JSON Schema's `atrHash` and `clauseId` patterns** accepted lowercase
  hex only, rejecting documents the standard permits. Both now accept either
  case. Anyone pinning the published schema should expect previously-invalid
  uppercase documents to validate.

### Documented

Recording changes made after the 1.0 release that this changelog had not
carried:

- `81cc4f0` — generalized named ADR providers in the spec examples and removed
  AAA-ICDR's TSC seat while retaining it as Founding Maintainer.
- `df26157` — rephrased the Dispute Resolution working-group bullet.
- `f129a76` — corrected the ATR expansion to "Agentic Transaction **Record**".
  "Receipt" collided with the settlement receipt that carries `atrHash`.

---

## [1.0] — 2026-06-24

Initial public release of the Legal Context Protocol.

- **The Standard (§2).** Normative core: the `/.well-known/legal-context.json`
  discovery document, the single required `terms` field, and the optional field
  set (`termsFormat`, `atrHash`, `acceptanceRequired`, `disputeResolution`,
  `returns`, `contact`, `api`).
- **Levels of Trust (§3).** Advisory model — Informational, Provable, Signed,
  Integrated.
- **Buyer Policy (§4).** Advisory client-side counterpart to published terms.
- **Transaction-Time Verification (§5), Private and Custom Terms (§6), Content
  Storage (§7).**
- **Protocol Integration (§8).** Abstract, protocol- and chain-agnostic
  integration interface; the known reference-type registry; and the Settlement
  Binding Pattern vocabulary.
- **Relationship to Authorization Protocols (§9), MCP as Delivery Mechanism
  (§10).**
- **IANA Considerations (§11), Security Considerations (§12), References (§13).**
- **Appendices A–E.** Worked example, pattern illustrations, protocol
  integration illustrations, comparison matrix, and legal significance.
- **JSON Schema** for the discovery document and **Level 1–4 examples**.

Status: Draft — released for community review. Future changes proceed through the
SEP process (see [GOVERNANCE.md](GOVERNANCE.md)).
