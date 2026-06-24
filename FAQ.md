# FAQ & Glossary

A quick reference for the Legal Context Protocol (LCP). For the full normative text, see the [specification](spec/legal-context-protocol-v1.md).

## FAQ

**Do you need a blockchain to use LCP?**
No. Level 1 and Level 2 work on any web server serving a JSON file. Blockchains only come in when you bind the terms hash to an on-chain settlement.

**Is this "code is law"? Are you replacing lawyers or courts?**
The opposite. LCP's premise is that code *can't* be law — an agreement needs identity, consent, jurisdiction, and recourse, which code doesn't provide. LCP connects agent transactions *to* the existing legal system (including dispute-resolution institutions such as the American Arbitration Association), rather than replacing it.

**What stops someone changing the terms after the fact?**
The `atrHash` — a SHA-256 hash of the terms. If the document changes by one byte, the hash changes, and the mismatch is detectable by either party. The served terms file must be byte-identical every time.

**What about prompt injection in the terms text?**
A buyer's accept/reject decision should be made over the **structured fields** of `legal-context.json` (jurisdiction, level, amount), never the free-text terms body. Human escalation binds approval to the exact bytes' hash.

**Who controls LCP? Is it a single-vendor land-grab?**
LCP is an open standard (IANA-registered well-known URI, Apache-2.0), co-stewarded by **Integra Ledger** and the **American Arbitration Association**. By design, no central index, registry, or facilitator is operated by any one party — every "hosted" capability points to the adopter's own instance.

**How is this different from just posting a Terms of Service?**
Three things a `/terms` link doesn't give you: a **standard location** (so agents can find it), a **cryptographic proof** (so it can't be quietly changed), and a **signature + recourse path** (so it's enforceable).

**Is there a reference implementation?**
Yes — open-source `@legalcontext/*` packages and a live demo. LCP is designed for many implementations in any language, kept honest by language-neutral conformance vectors.

## Glossary

**LCP (Legal Context Protocol)** — an open standard for publishing and cryptographically proving the legal terms of a transaction, for AI-agent commerce. One required field; four optional trust levels.

**ATR (Agentic Transaction Receipt)** — the terms document itself (the standalone, downloadable file). The thing that gets hashed.

**`atrHash`** — the SHA-256 hash of the terms bytes (`0x` + 64 hex). The tamper-evident fingerprint binding terms ↔ seller ↔ buyer's transaction.

**`/.well-known/legal-context.json`** — the standardized HTTPS URL where any service publishes its LCP record.

**The four levels** — **L1 Informational** (terms at a known URL) · **L2 Provable** (+ `atrHash`) · **L3 Signed** (+ buyer signature over the hash) · **L4 Integrated** (+ dispute resolution, jurisdiction, API).

**Buyer Policy** — the client-side rules an agent uses to decide whether to accept terms (minimum level, allowed jurisdictions/dispute methods, spend caps, signing thresholds), evaluated over structured fields only.

**Binding pattern** — how the `atrHash` is attached to a settlement on a given chain: **Native Field, Overlay Contract, Sidecar Attestation, Opaque Challenge, Id-Reuse, Protocol Extension** (+ an HTTP-layer advisory baseline).

**Native Field** — the cheapest, most common binding: the hash rides in a field the chain already exposes (a memo, metadata label, or muxed-account id) — no new contract.

**Overlay Contract** — a small contract that wraps settlement to emit the hash; used only where a chain has no native carrier.

**Anchoring** — optional proof of *when* terms were published (on-chain tx, content-addressed storage, or RFC-3161 timestamp).

**Rail** — a settlement ledger or channel (EVM, Stellar, Hedera, Sui, Solana, Aptos, XRPL, Cardano, Canton, and traditional rails).

**Settlement vs. reference-carrier protocols** — *settlement* protocols (x402, MPP, AP2, ACK) move value; *reference-carrier* protocols (ACP, UCP, Visa-TAP, Mastercard-VI, A2A, MCP) carry the LCP reference so agents become LCP-aware.

**Conformance vector** — a language-neutral JSON test case (fixed inputs → exact expected output) that lets any implementation, in any language, prove byte-compatibility.

**x402 / MPP / AP2 / ACK** — agent-payment protocols LCP integrates with (Coinbase x402; Machine Payments Protocol; Agent Payments Protocol; Agent Commerce Kit).
