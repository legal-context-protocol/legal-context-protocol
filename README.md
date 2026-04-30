<img src="lcp-icon.svg" alt="Legal Context Protocol" width="120" />

# Legal Context Protocol (LCP)

An open standard for discovering the legal context of agentic commerce transactions.

---

## What Is LCP?

AI agents are transacting autonomously. Every major agentic commerce protocol — MPP, ACP, x402, UCP, AP2, Visa TAP, Mastercard Agent Pay — handles payments and authorization. None addresses the legal layer: what were the terms? What is the dispute process? Who has jurisdiction?

LCP fills this gap. A service publishes a single JSON file at a well-known URL:

```
https://{domain}/.well-known/legal-context.json
```

One required field. Everything else is optional.

## Quick Start

### Minimal (Level 1)

```json
{
  "terms": "https://example.com/terms/v3.md"
}
```

Save as `legal-context.json` and serve at `/.well-known/legal-context.json` over HTTPS. That's it.

### With Hash Verification (Level 2)

```json
{
  "terms": "https://example.com/terms/v3.md",
  "atrHash": "0x7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"
}
```

### With Signed Acceptance (Level 3)

```json
{
  "terms": "https://example.com/terms/v3.md",
  "atrHash": "0x7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
  "acceptanceRequired": true
}
```

When `acceptanceRequired` is `true`, the counterparty digitally signs the terms (e.g., via EIP-712) before transacting — cryptographic proof of consent.

### Full (Level 4)

See [`examples/level-4-full.json`](examples/level-4-full.json) for a complete configuration with dispute resolution, contact information, and API integration.

## Specification

- **Full specification:** [`spec/legal-context-protocol-v1.md`](spec/legal-context-protocol-v1.md)
- **JSON Schema:** [`spec/legal-context.schema.json`](spec/legal-context.schema.json)
- **Examples:** [`examples/`](examples/)
- **Website:** [www.legalcontextprotocol.org](https://www.legalcontextprotocol.org)

## Four Levels of Trust

| Level | Name | What It Adds |
|-------|------|-------------|
| 1 | Informational | Terms are discoverable at a known URL |
| 2 | Provable | An ATR hash proves the terms haven't changed |
| 3 | Signed | Cryptographic proof of explicit consent |
| 4 | Integrated | Dispute resolution, pre-settlement verification, escrow, reputation, and other recourse hooks |

Each level is independently valuable. A service can implement any level without implementing the others.

## Buyer Policy

Level 3 (signed acceptance) is bilateral: the service publishes terms, and the buyer's principal declares a policy that decides whether those terms are acceptable. A buyer policy encodes minimum trust level, acceptable jurisdictions, acceptable dispute methods, commitment caps, and signing thresholds — and gates the agent's signing key behind human review for commitments above the threshold. See [Specification §4](spec/legal-context-protocol-v1.md#4-buyer-policy) for the policy primitives, evaluation flow, and human-in-the-loop escalation.

## Protocol Integration

LCP integrates with the major agentic commerce and authorization protocols in two tiers: mechanisms that work today against stock, unmodified protocols using existing extension surfaces (Tier A), and mechanisms that require upstream specification changes (Tier B). Specification §8 and Appendix C have the full detail:

- **§8.3 On-Chain Binding Patterns** defines the pattern vocabulary — Native Field, Overlay Contract, Sidecar Attestation, Opaque Challenge, Id-Reuse, Protocol Extension — with two evaluation axes (wire compatibility, adoption cost) and three recovery properties (on-chain, zero-party recoverable, forward-indexable).
- **Appendix C — Protocol Integration Illustrations** identifies the integration surfaces for each protocol and credential type, with Tier A/B labeling and steward invitations.

Per-chain bindings (Stellar `mux_id`, Tempo TIP-20 memo, EVM overlay contracts) are deliberately not canonized in the spec — chain operators are invited to publish authoritative profiles in their own documentation.

| Protocol | Integration surface | Tier |
|----------|---------------------|------|
| MPP | LCP fields inside the HMAC-covered `request.methodDetails` body | A — Available today |
| MPP | First-class `legalContext` on `WWW-Authenticate: Payment` header or `Payment-Receipt` | B — Proposed |
| ACP | Freeform session metadata / `links` array | A — Available today |
| ACP | Formal `capabilities.extensions[]` registration (SEP) | B — Proposed |
| UCP | `links` array with `terms_of_service` type (Level 1 discovery only) | A — Available today |
| UCP | `allOf` schema extension with reverse-domain naming | B — Proposed |
| x402 | `accepts[].extra` per-requirement block and top-level `extensions` in v2 | A — Available today |
| x402 | First-class `legalContext` field on `PAYMENT-RESPONSE` receipts | B — Proposed |
| AP2 | Alongside mandates in transport metadata | A — Available today |
| AP2 | Embedded as a field within a signed mandate | B — Proposed |
| Visa TAP | Custom HTTP header (e.g. `X-LCP-Hash`) — advisory only, not covered by signature chain | A — Available today |
| Visa TAP | Field inside an existing signed object, or a sibling with its own signature quartet | B — Proposed |
| Mastercard Verifiable Intent | Custom Layer 2 constraint type (URN / reverse-domain namespaced) | A — Available today |
| A2A | Task metadata (arbitrary) and Agent Card `extensions` (§4.6) | A — Available today |
| MCP | Tools, resources, and prompts on an LCP-aware MCP server | A — Available today |

## Governance

LCP is co-stewarded by **Integra Ledger** and the **American Arbitration Association-International Centre for Dispute Resolution (AAA-ICDR)** as Founding Maintainers.

- **Open standard, open source.** Apache 2.0 licensed. No fees at any level.
- **Contribution-based TSC.** Up to 7 seats, earned through contributions.
- **Transparent process.** All changes via public SEPs with community review.
- **No exclusivity.** Participants are free to work with any other protocol.

See [GOVERNANCE.md](GOVERNANCE.md) for the full governance framework.

## Contributing

We welcome contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

All contributors must sign a [Contributor License Agreement](legal/cla/) before contributions can be accepted.

## License

[Apache License 2.0](LICENSE)
