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
  "terms": "https://example.com/terms/v3.pdf"
}
```

Save as `legal-context.json` and serve at `/.well-known/legal-context.json` over HTTPS. That's it.

### With Hash Verification (Level 2)

```json
{
  "terms": "https://example.com/terms/v3.pdf",
  "contentHash": "0x7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"
}
```

### With Signed Acceptance (Level 3)

```json
{
  "terms": "https://example.com/terms/v3.pdf",
  "contentHash": "0x7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
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
| 2 | Provable | A content hash proves the terms haven't changed |
| 3 | Signed | Cryptographic proof of explicit consent |
| 4 | Integrated | Dispute resolution, escrow, compliance hooks |

Each level is independently valuable. A service can implement any level without implementing the others.

## Protocol Integration

LCP integrates with every major agentic commerce protocol via existing extension mechanisms:

| Protocol | Integration Mechanism |
|----------|----------------------|
| MPP | `legalContext` field in 402 challenges and receipts |
| ACP | Formal extension via `capabilities.extensions[]` |
| x402 | `extensions.legalContext` in PaymentRequired responses |
| UCP | `com.integra.legal-context` schema extension |
| Visa TAP | `legalContext` in signed request body |
| A2A | Agent Card extensions and task metadata |
| MCP | Tool annotations for legally significant actions |
| AP2 | Alongside mandates in transport metadata |
| Mastercard VI | Legal constraints in Layer 2 credentials |

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
