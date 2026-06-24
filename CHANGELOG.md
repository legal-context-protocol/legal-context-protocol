# Changelog

All notable changes to the Legal Context Protocol are recorded here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The
specification edition is carried in the document header; repository releases are
tagged to match.

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
