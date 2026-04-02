# Legal Context Protocol

**Version:** 0.1-draft
**Date:** March 30, 2026
**Authors:** David Fisher (Integra Ledger), David Berger
**Status:** Draft
**License:** Apache 2.0

---

## Abstract

This document specifies the Legal Context Protocol (LCP), an open standard for discovering the legal context of agentic commerce transactions. The standard defines a well-known URI (`/.well-known/legal-context.json`) where any service publishes a reference to its legal terms. The standard requires no specific technology — no blockchain, no cryptography, no API, no third-party service. Any web server can implement it.

Beyond the normative core, this document provides advisory guidance for increasing levels of trust assurance: provable terms, signed acceptance, and integration with legal infrastructure such as dispute resolution and escrow systems.

For the conceptual framework motivating this standard — why agentic commerce requires legal context and what that means — see the companion white paper: *"Identity, Trust, and the Legal Foundations of Agentic Commerce"* (Fisher & McCormack, 2026).

## Status of This Document

This is a draft specification for community review. The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119].

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [The Standard](#2-the-standard)
3. [Levels of Trust](#3-levels-of-trust)
4. [Transaction-Time Verification](#4-transaction-time-verification)
5. [Private and Custom Terms](#5-private-and-custom-terms)
6. [Content Storage](#6-content-storage)
7. [Protocol Integration](#7-protocol-integration)
8. [Relationship to Authorization Protocols](#8-relationship-to-authorization-protocols)
9. [MCP as Delivery Mechanism](#9-mcp-as-delivery-mechanism)
10. [IANA Considerations](#10-iana-considerations)
11. [Security Considerations](#11-security-considerations)
12. [References](#12-references)

---

## 1. Introduction

For agentic commerce to reach its full potential, transactions need legal context.

AI agents are transacting autonomously — purchasing services, accessing APIs, executing procurement, settling payments. The payment infrastructure works. The commerce protocols work. The identity protocols work. But none of them address what happens when a transaction goes wrong: what were the terms? Did the counterparty consent? What is the dispute process? Who has jurisdiction?

The companion white paper, *"Identity, Trust, and the Legal Foundations of Agentic Commerce"* (Fisher & McCormack, 2026), defines what legal context means for the agentic era:

- **Jurisdiction** — every transaction must be connected to a governing legal framework
- **Terms** — recorded permanently, independently verifiable, controlled by neither party
- **Temporal obligations** — liability allocation, performance standards, breach remedies, implied warranties, and method of recourse that extend beyond the moment of exchange
- **Evidentiary integrity** — a neutral, independently verifiable record
- **Intent** — connection back to human deliberation and consent

Today, none of this is discoverable. An agent transacting with a service has no standard way to find the legal context governing that transaction. Legal terms are scattered across `/terms`, `/tos`, `/legal/terms-of-service`, buried in PDFs, or absent entirely. There is no convention.

The agentic commerce ecosystem has invested heavily in payment infrastructure — MPP, ACP, x402, UCP, AP2, Visa TAP, Mastercard Agent Pay — and in authorization infrastructure — Verifiable Intent, AP2 mandates, TAP signatures. But no protocol addresses the merchant's side of the transaction: what terms were offered, what obligations were accepted, what recourse is available. LCP fills this gap.

This standard solves the first and most fundamental problem: **discoverability**. Legal terms are always in the same place. Everything else — verification, acceptance, enforcement, dispute resolution — can be built on top of discoverability. But without it, nothing else is possible.

---

## 2. The Standard

### 2.1 Well-Known URI

A service implementing this standard MUST serve a JSON document at:

```
https://{domain}/.well-known/legal-context.json
```

The document MUST be served over HTTPS. The TLS certificate provides domain identity anchoring.

### 2.2 File Format

The discovery document MUST be valid JSON (`application/json`).

### 2.3 Legal Terms Are a Document

The legal terms referenced in `legal-context.json` MUST be a standalone file — a discrete, downloadable artifact. Not a section of a webpage. Not dynamically rendered HTML. The file format does not matter: PDF, Word, Markdown, JSON, plain text, or any other format. The file being a self-contained, downloadable artifact is the requirement.

The file MUST be served via standard HTTP(S) `GET`. The server SHOULD include a `Content-Type` header declaring the file format.

### 2.4 Required Fields

```json
{
  "terms": "https://example.com/terms/v3.pdf"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `terms` | string | REQUIRED | Absolute HTTPS URL of the legal terms document. MUST return a standalone, downloadable file. For services with only confidential/private terms, this URL MAY return a document stating that terms are provided at transaction time (see Section 5.1). |

### 2.5 Optional Fields

```json
{
  "terms": "https://example.com/terms/v3.json",
  "termsFormat": "agentic-transaction-record-v1",
  "contentHash": "0x7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
  "hashAlgorithm": "sha256",
  "acceptanceRequired": false,
  "disputeResolution": {
    "method": "AAA Commercial Arbitration Rules",
    "jurisdiction": "New York, USA",
    "contact": "disputes@example.com",
    "clauseId": "sha256:0x<hash>",
    "source": "https://adr.org/clauses/commercial-arbitration",
    "catalog": "https://adr.org/.well-known/dispute-services.json"
  },
  "returns": "https://example.com/api/returns",
  "contact": {
    "legal": "legal@example.com",
    "technical": "api-support@example.com"
  },
  "api": "https://api.integraledger.net/v1/records/0xabcdef1234567890"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `termsFormat` | string | OPTIONAL | The format or schema of the terms document. Signals to agents whether the terms are machine-readable before fetching. Known values: `"agentic-transaction-record-v1"`, `"pdf"`, `"markdown"`, `"html"`, `"plain"`. When absent, agents determine format from the `Content-Type` header after fetching. |
| `contentHash` | string | OPTIONAL | SHA-256 hash of the terms document, `0x`-prefixed hex (66 characters). See [Level 2](#level-2-provable). |
| `hashAlgorithm` | string | OPTIONAL | Hash algorithm used. Defaults to `"sha256"` if `contentHash` is present. |
| `acceptanceRequired` | boolean | OPTIONAL | If `true`, counterparties MUST explicitly accept terms before transacting. See [Level 3](#level-3-signed). Default: `false`. |
| `disputeResolution` | object | OPTIONAL | Dispute resolution process. See [Level 4](#level-4-integrated). |
| `disputeResolution.method` | string | OPTIONAL | The dispute resolution method (e.g., "AAA Commercial Arbitration Rules"). |
| `disputeResolution.jurisdiction` | string | OPTIONAL | Governing jurisdiction. |
| `disputeResolution.contact` | string | OPTIONAL | Contact for dispute filing. |
| `disputeResolution.clauseId` | string | OPTIONAL | Content-addressed identifier of the dispute resolution clause. Format: `sha256:0x<hex>`. When present, the clause is verifiable — any party can retrieve the text and confirm it matches the hash. |
| `disputeResolution.source` | string | OPTIONAL | URL where the dispute resolution clause text can be retrieved. Any resolvable URI (HTTPS, IPFS, Arweave, etc.). |
| `disputeResolution.catalog` | string | OPTIONAL | URL of the dispute resolution provider's service catalog. When present, agents can browse offerings, parameters, and constraints, and generate customized clause specifications programmatically. |
| `returns` | string | OPTIONAL | URL of a returns or claims API/process. |
| `contact` | object | OPTIONAL | Contact information for the service. |
| `contact.legal` | string | OPTIONAL | Legal department contact. |
| `contact.technical` | string | OPTIONAL | Technical support contact. |
| `api` | string | OPTIONAL | URL of a legal context API providing richer functionality (record management, verification, dispute filing). See [Level 4](#level-4-integrated). |

The field set is extensible. Implementations SHOULD ignore fields they do not recognize.

### 2.6 Serving Requirements

The discovery document MUST be served over HTTPS.

Clients SHOULD cache the discovery document for a period not exceeding 24 hours. Clients MUST re-fetch after cache expiry. Vendors MAY include standard HTTP cache headers (`Cache-Control`, `ETag`, `Last-Modified`).

### 2.7 Examples

**Minimal (Level 1):**
```json
{
  "terms": "https://example.com/terms/v3.pdf"
}
```

**With content hash (Level 2):**
```json
{
  "terms": "https://example.com/terms/v3.pdf",
  "contentHash": "0x7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069"
}
```

**With signed acceptance (Level 3):**
```json
{
  "terms": "https://example.com/terms/v3.pdf",
  "contentHash": "0x7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
  "acceptanceRequired": true
}
```

When `acceptanceRequired` is `true`, the counterparty must digitally sign the terms before transacting — for example, using EIP-712 typed data signing. This creates cryptographic proof that a specific party explicitly consented to specific terms at a specific time.

**Full (Level 4):**
```json
{
  "terms": "https://example.com/terms/v3.json",
  "termsFormat": "agentic-transaction-record-v1",
  "contentHash": "0x7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
  "acceptanceRequired": true,
  "disputeResolution": {
    "method": "AAA Commercial Arbitration Rules",
    "jurisdiction": "New York, USA",
    "contact": "disputes@example.com",
    "clauseId": "sha256:0x<hash>",
    "source": "https://adr.org/clauses/commercial-arbitration",
    "catalog": "https://adr.org/.well-known/dispute-services.json"
  },
  "returns": "https://example.com/api/returns",
  "contact": {
    "legal": "legal@example.com",
    "technical": "api-support@example.com"
  },
  "api": "https://api.integraledger.net/v1/records/0xabcdef1234567890"
}
```

---

## 3. Levels of Trust

*This section is advisory. Nothing in this section is required for conformance with the standard. The standard (Section 2) is the normative core.*

Beyond the standard location, this specification suggests approaches at increasing levels of trust assurance. Each level is independently valuable. A vendor can implement any level without implementing the others. Higher levels naturally incorporate the capabilities of lower levels.

### Level 1: Informational

An agent can find the published terms and conditions of a service. The terms are readable at a known URL. Proceeding with a transaction after discovering the terms constitutes affirmative consent — consistent with the legal framework for browsewrap/clickwrap agreements under U.S. law (supported by the Uniform Electronic Transactions Act (UETA § 14) and the Electronic Signatures in Global and National Commerce Act (E-SIGN, 15 U.S.C. § 7001 et seq.)) and EU law (the E-Commerce Directive 2000/31/EC and eIDAS Regulation (EU) No 910/2014).

The `legal-context.json` file points to the terms document. An agent or human that transacts after discovering the terms has implicitly accepted them. No hash, no blockchain, no signature needed.

### Level 2: Provable

For greater trust, the legal context includes digital proof of the terms. The `legal-context.json` file includes a `contentHash` field — a SHA-256 hash of the terms document. This proves:

- **What the terms were** — the hash identifies the exact document
- **That they haven't changed** — any modification breaks the hash

If a `contentHash` is provided, the terms document MUST be byte-for-byte identical every time it is served. No dynamic content insertion, no session-specific rendering, no content negotiation that changes the response. Any party that downloads the file and computes SHA-256 MUST get the same hash.

Optionally, the hash may be anchored to a blockchain, a timestamp authority ([RFC 3161]), or content-addressed storage (IPFS, Arweave) to prove *when* the terms were published. The hash alone — without any anchoring — provides provability. Anyone with the document can verify it matches the hash.

### Level 3: Signed

For explicit consent, the counterparty digitally signs the terms — for example, using EIP-712 typed data signing or a similar standard. This adds proof of intent: not only are the terms provable (Level 2), but there is cryptographic evidence that a specific party explicitly consented to those specific terms at a specific time.

This is the digital equivalent of a signed contract. The signature binds an identity to a document.

When `acceptanceRequired` is `true` in `legal-context.json`, the service signals that it requires explicit acceptance before transacting.

### Level 4: Integrated

For complex transactions, the `legal-context.json` file includes hooks to richer legal infrastructure:

- **Dispute resolution systems** — structured processes, institutional arbitration (e.g., AAA)
- **Escrow and conditional payment release** — programmatic enforcement of conditions
- **Multi-party agreement management** — buyer, seller, agents, principals
- **Identity verification** — party attestation and authorization chains
- **Compliance gating** — regulatory enforcement
- **Returns and claims processes** — operational automation
- **Access-controlled private terms** — gated access for confidential agreements

At this level, the terms may not be publicly readable. Access may be gated — only authenticated parties can retrieve private terms. The `api` field in `legal-context.json` provides the entry point to this richer functionality.

Level 4 is not specific to any single implementation. Any legal infrastructure reachable via an API endpoint qualifies. The standard provides the hook; the implementation provides the capability.

---

## 4. Transaction-Time Verification

*This section is advisory.*

### 4.1 Two Moments

**Discovery time** — The agent visits `/.well-known/legal-context.json` to understand how a service handles legal terms. This is informational. The agent may browse terms, evaluate the vendor, and decide whether to engage.

**Transaction time** — The correct moment to fetch, verify, and save the terms. This is when the `contentHash` matters (Level 2+).

### 4.2 The Proposal-Phase Pattern

Every major agentic commerce protocol has a two-phase flow — propose, then execute:

| Protocol | Proposal Phase | Execution Phase |
|----------|---------------|-----------------|
| MPP | 402 challenge | Payment credential + 200 receipt |
| ACP | Checkout session creation | Complete checkout |
| x402 | 402 response | Payment + resource delivery |
| UCP | Checkout session creation | Payment confirmation + order |
| AP2 | Cart/Intent Mandate creation | Payment Mandate + authorization |

At Level 2+, the `contentHash` SHOULD be included in the proposal phase. Including it in the proposal allows the agent to verify before paying. Including it only in the receipt is valid but weaker — the agent cannot verify before committing.

### 4.3 Agent Verification Flow (Level 2+)

1. Receive the proposed `contentHash` from the server (in the proposal)
2. Fetch the terms document from the URL provided
3. Compute SHA-256 of the downloaded document
4. Compare to the proposed `contentHash` — **if mismatch, halt**
5. Save the document locally
6. Proceed with payment
7. Receive receipt containing the same `contentHash` — confirmation of what was agreed

This eliminates both race conditions (terms changed between discovery and transaction) and malice (server claiming different terms after the fact). The agent verifies at the moment that matters — right before it pays.

### 4.4 Level 1 Behavior

At Level 1 (no hash), there is no `contentHash` in the proposal. The terms URL from `legal-context.json` is the reference. The agent should still fetch and save the terms at transaction time as evidence of what it saw, even without a hash to verify against. At Level 1, the discovery-time terms and the transaction-time terms are assumed to be the same; the agent has no mechanism to detect a change between discovery and transaction.

### 4.5 Document Preservation

Agents SHOULD save a copy of the terms at transaction time regardless of level. At Level 2+, agents SHOULD verify the `contentHash` against the downloaded document before proceeding.

The vendor does not need to guarantee long-term availability of the document at the URL. The document only needs to be downloadable when the agent transacts. After that, the proof lives with the parties — the document in their possession and the hash in the receipt.

A hash without a document is a proof without evidence.

---

## 5. Private and Custom Terms

*This section is advisory.*

### 5.1 The Ephemeral Link Pattern

The transaction-time model naturally solves the privacy problem. A seller can propose completely custom, private terms for a specific transaction:

1. Server generates custom terms for this buyer/transaction
2. Server computes the `contentHash`
3. Server includes the `contentHash` in the proposal along with an ephemeral link to the document (this transaction-specific URL overrides the permanent URL from `legal-context.json`)
4. Agent downloads the document from the ephemeral link
5. Agent verifies the hash matches
6. Agent saves the document locally
7. Agent proceeds with transaction
8. Ephemeral link expires — the document is gone from the server

The terms were never public. No permanent URL. No access control system needed. No encryption. No key management. The document existed at one URL for long enough for the buyer to download, and then it's gone. Both parties have a copy. The `contentHash` in the receipt is the proof.

This naturally supports:
- **NDAs and confidential agreements** — only the two parties ever see the terms
- **Custom per-customer pricing and terms** — every proposal can have different terms with a different `contentHash`
- **Settlement agreements** — terms exist only between the parties
- **Dynamically generated terms** — assembled at proposal time based on the specific transaction

### 5.2 Encrypted Persistent Storage

For private terms that require long-term storage (not ephemeral), the document may be encrypted before storage. In this case: **hash the plaintext, then encrypt.**

The `contentHash` SHOULD always identify the *content* — what the terms actually say — not a specific encrypted artifact. This means:
- Any party with access to the decrypted document can verify the `contentHash`
- The same terms encrypted with different keys or for different recipients have the same `contentHash`
- Key rotation or re-encryption does not break the hash
- Dispute resolution is straightforward: present the plaintext, hash it, compare to the `contentHash` on record

### 5.3 Privacy Note

The same `contentHash` appearing across multiple transactions only reveals a correlation if those transactions are publicly broadcast (e.g., on a public blockchain). Most agentic commerce transactions are private HTTP exchanges between two parties. The `contentHash` in protocol metadata is visible only to the transacting parties. This is not a privacy concern unless transactions are publicly broadcast.

---

## 6. Content Storage

*This section is advisory.*

The `legal-context.json` file points to the terms. Where and how those terms are stored affects trust, availability, and verifiability. This specification does not mandate a storage approach.

### 6.1 Vendor-Hosted

The terms live on the vendor's own web server. The vendor controls the content and can update it at any time. Suitable for Level 1. The weakness: the vendor can change the document and no one can prove what it said before.

### 6.2 Content-Addressed Storage

The document is stored at an address derived from its content (e.g., IPFS, Arweave). The address IS the hash. If the content changes, the address changes. Suitable for Level 2+ — the storage itself provides the integrity guarantee. IPFS requires pinning for availability; Arweave provides permanence at a cost.

### 6.3 Third-Party Archival

A neutral third party stores a snapshot of the terms — the exact bytes at a point in time. The snapshot can be hashed and verified. Suitable for Levels 2-4. The trust model shifts to the archival provider.

### 6.4 On-Chain Storage

The full document stored on-chain (calldata or blob). Permanent and immutable but expensive. Practical only for short documents or high-value agreements.

### 6.5 Encrypted Storage

For persistent private terms (Level 4). See Section 5.2 for the hash-then-encrypt recommendation.

---

## 7. Protocol Integration

*This section is advisory.*

This section describes how legal context references can be embedded in existing agentic commerce protocols. No protocol requires core specification changes. All integrations use existing extension mechanisms.

### 7.1 Naming Conventions

The protocols are structurally different, so a single wire format cannot apply everywhere. The recommendations:

**String fields** (e.g., MPP `opaque`, ACP metadata values): Use the `lcp:` prefix with a type indicator:

```
lcp:{type}:{value}
```

Self-identifying — any parser checks `startsWith("lcp:")`, then reads the type to know how to resolve the value.

**Parsing rule:** Split on the first colon to get `lcp` (the namespace). Split on the second colon to get the type. Everything after the second colon is the value (which may itself contain colons, e.g., in URLs).

**Structured JSON** (e.g., ACP session metadata, A2A task metadata, UCP extensions): Use a standard key — `"legalContext"` — with `type` and `value` fields:

```json
{
  "legalContext": {
    "type": "sha256",
    "value": "0x7f83b165..."
  }
}
```

**Raw byte fields** (e.g., TIP-20 32-byte memo): No prefix — there is no room. The per-protocol integration guide defines the meaning.

### 7.2 Known Types

The type set is extensible. This is not a closed set.

| Type | Value Format | Example |
|------|-------------|---------|
| `sha256` | Content hash, `0x`-prefixed hex | `lcp:sha256:0x7f83b165...` |
| `ipfs` | IPFS CID | `lcp:ipfs:QmYwAPJzv5CZsnA...` |
| `ar` | Arweave transaction ID | `lcp:ar:bNbA3DWNQJ...` |
| `url` | URL to terms or `legal-context.json` | `lcp:url:https://example.com/terms/v3.pdf` |
| `integra` | Integra record reference | `lcp:integra:0xabcdef...` |

### 7.3 Per-Protocol Integration

Each protocol integration specifies:
- The exact field to use
- The format (string prefix, JSON key, or raw bytes)
- When in the protocol flow it is set (proposal phase for `contentHash`)
- Size constraints
- How the receiving party reads and resolves the value
- Code examples

#### MPP (Machine Payments Protocol)

MPP is an open standard (IETF Internet-Draft, Apache 2.0), co-authored by Stripe and Tempo Labs. It enables machine-to-machine payments via HTTP 402 challenges, supporting stablecoins on Tempo, cards via Stripe, and Bitcoin via Lightning.

We recommend adding a dedicated `legalContext` field rather than overloading existing fields.

**In the 402 challenge (proposal phase):**
```
WWW-Authenticate: Payment id="abc123", realm="api.example.com",
  method="tempo", intent="charge", request="eyJhb...",
  legalContext="lcp:url:https://example.com/terms/v3.pdf"
```

> **Note:** MPP authenticates the 402 challenge via HMAC. Adding a `legalContext` parameter means it MUST be included in the HMAC computation; otherwise the client cannot verify challenge integrity. This requires a coordinated change to the MPP specification.

**In the payment receipt (execution phase):**
```json
{
  "method": "tempo",
  "status": "success",
  "reference": "0x...",
  "timestamp": "2026-03-20T14:30:00Z",
  "legalContext": {
    "type": "sha256",
    "value": "0x7f83b165..."
  }
}
```

> **Note:** The receipt JSON shown above is the decoded content. In the MPP flow, this is base64url-encoded and transmitted in the `Payment-Receipt` header.

Backward compatible — clients that do not understand `legalContext` ignore it. This change can be submitted upstream as a PR to the MPP specification.

**MPP Sessions:** MPP supports session-based streaming micropayments where an agent authorizes a spending limit upfront and streams payments against the session. For session-based payments, the `legalContext` SHOULD be included in the session establishment (the initial 402 challenge that creates the session) rather than in each individual streamed payment. All payments within a session are governed by the terms established at session creation.

**TIP-20 memo (32 bytes):** The raw SHA-256 content hash can be placed directly in the memo field for on-chain binding. No type prefix — the field's purpose is defined by the integration guide.

> **Note:** MPP's SDK auto-generates an attribution memo in the TIP-20 memo field only when no user-provided memo is present. Providing a contentHash as the memo replaces MPP's default attribution — this is the intended behavior for LCP-enabled transactions. The `legalContext` field in the receipt provides the same binding at the protocol level; the TIP-20 memo provides additional on-chain binding.

#### ACP (Agentic Commerce Protocol)

ACP is an open-source specification (Apache 2.0) co-maintained by OpenAI and Stripe. Version 2026-01-30 introduced a formal extensions mechanism.

We recommend submitting a Specification Enhancement Proposal (SEP) to register LCP as a formal ACP extension, rather than using freeform session metadata.

**As an ACP extension:**

The `legalContext` extension would be declared in `capabilities.extensions[]` during session establishment and negotiated between agent and seller:

```json
{
  "capabilities": {
    "extensions": ["com.integra.legal-context"]
  }
}
```

**In checkout session responses:**
```json
{
  "legalContext": {
    "type": "sha256",
    "value": "0x7f83b165..."
  }
}
```

ACP checkout responses already include a `links` array with `terms_of_use`, `privacy_policy`, and `return_policy` as plain URLs. The LCP extension upgrades these from informational URLs to hash-verified, integrity-protected terms references. The `links` array continues to serve as the Level 1 (informational) integration point; the `legalContext` extension adds Level 2+ capabilities.

#### x402

x402 is an HTTP 402-based payment protocol co-founded by Cloudflare and Coinbase (x402 Foundation), now including Google and Visa.

> **Note:** This targets x402 v2, which introduces a native `extensions` field in PaymentRequired responses.

**Option 1 — Custom response header:**
```
X-LCP-Hash: 0x7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
```

**Option 2 (recommended) — x402 v2 `extensions` field:**
```json
{
  "extensions": {
    "legalContext": {
      "type": "sha256",
      "value": "0x7f83b165..."
    }
  }
}
```

The `extensions` field is the preferred integration point as it is part of the x402 v2 PaymentRequired schema and does not require custom headers. x402 v2 also supports reusable sessions — as with MPP, the `legalContext` SHOULD be established at session creation and governs all payments within the session.

#### UCP (Universal Commerce Protocol)

UCP is an open-source standard (Apache 2.0) co-developed by Google with Shopify, Etsy, Wayfair, Target, and Walmart. It covers the full commerce lifecycle: discovery, catalog, checkout, orders, fulfillment, and post-purchase adjustments. UCP uses a composable extension architecture and publishes its own well-known discovery file at `/.well-known/ucp`.

**LCP as a UCP extension:**

UCP requires formal `allOf` schema extensions using reverse-domain naming conventions. Legal context would be registered as:

```json
{
  "extensions": {
    "com.integra.legal-context": {
      "type": "sha256",
      "value": "0x7f83b165...",
      "disputeResolution": {
        "method": "AAA Commercial Arbitration Rules",
        "jurisdiction": "New York, USA"
      }
    }
  }
}
```

**Relationship to UCP's existing `links` array:** UCP checkout responses require `privacy_policy` and `terms_of_service` URLs in the `links` array. These serve as the Level 1 (informational) integration — the terms are discoverable. The LCP extension adds Level 2+ capabilities (content hash, signed acceptance, dispute resolution hooks) without replacing the existing `links` requirement.

**Relationship to UCP's Buyer Consent extension:** UCP provides a Buyer Consent extension (`ucp.dev/specification/buyer-consent/`) for declarative consent capture. LCP Level 3 (signed acceptance) provides cryptographic consent — a stronger, verifiable form. The two can coexist: Buyer Consent for UCP-level declarative consent, LCP Level 3 for cryptographic proof of acceptance.

**Relationship to UCP's Adjustments:** UCP logs post-purchase events including `dispute` as adjustment types, but provides no dispute resolution mechanism. LCP Level 4's `disputeResolution` field and `api` endpoint provide the mechanism that UCP's dispute adjustment logs feed into.

#### Visa TAP (Trusted Agent Protocol)

Visa TAP is an open framework built on RFC 9421 HTTP Message Signatures, co-developed with Cloudflare. It uses a three-signature model to establish agent identity, consumer identity, and payment authorization in every transaction. The protocol, its specifications, and a reference implementation are publicly available on the Visa Developer Center and GitHub.

TAP applies signatures during two interaction types: browsing (`agent-browser-auth` tag) and payment (`agent-payer-auth` tag). Each interaction can include three signed components:

1. **Agent Recognition Signature** — HTTP header signature proving the agent is Visa-trusted, domain-bound, time-bounded (max 8 minutes), and replay-protected via nonce
2. **Agentic Consumer Recognition Object** — request body containing consumer identity (JWT `idToken` with obfuscated email/phone) and contextual data (country, postal code, device), signed with the same private key and nonce as the agent signature
3. **Agentic Payment Container** — request body containing payment data (credential hash, encrypted payload, or browsing IOU), also signed with the same key and nonce

**LCP integration mechanism — request body with linked signature:**

TAP's body objects (Consumer Recognition, Payment Container) are each independently signed with the same private key and nonce used for the HTTP Message Signature, creating a cryptographic chain linking all components. The recommended integration follows this same pattern — include the LCP reference in the TAP request body and sign it with the same key and nonce:

```json
{
  "consumerRecognition": { ... },
  "paymentContainer": { ... },
  "legalContext": {
    "type": "sha256",
    "value": "0x7f83b165..."
  }
}
```

The shared key and nonce cryptographically bind the legal context to the agent identity, consumer identity, and payment data — proving not only *who* initiated the transaction and *that they were authorized*, but also *what terms governed it*. This follows the same signature-linking pattern TAP uses for its existing body objects.

**Alternative — custom header in covered components:**

Include `X-LCP-Hash` as a custom header. If added to the TAP signature's covered components in the `Signature-Input` header, it would be cryptographically bound to the agent's identity. This is simpler but carries only the hash, not structured legal context. Note: adding custom headers to TAP's covered components would require a coordinated extension to the TAP specification.

**Browsing IOU integration:** TAP's Browsing IOU mechanism (HTTP 402 deferred payment) creates a credit relationship — the merchant grants access with the expectation of later settlement. This deferred obligation is precisely the kind of temporal commitment that benefits from LCP: the IOU should reference specific terms governing the deferred payment, including what happens if settlement fails.

#### A2A (Agent-to-Agent Protocol)

A2A is an open protocol (Apache 2.0) enabling communication between AI agents. Created by Google, now governed by the Agentic AI Foundation (AAIF) under the Linux Foundation, with nearly 150 member organizations. Version 1.0 supports JSON-RPC, gRPC, and HTTP/REST bindings.

**Agent Card extension — publishing legal requirements:**

A2A agents discover each other via Agent Cards published at `/.well-known/agent-card.json`. An LCP-aware agent can declare its legal context requirements in its Agent Card, enabling programmatic compatibility assessment before interaction begins:

```json
{
  "name": "Procurement Agent",
  "skills": [...],
  "legalContext": {
    "required": true,
    "minimumLevel": 2,
    "acceptedJurisdictions": ["New York, USA", "London, UK"],
    "acceptedDisputeMethods": ["AAA Commercial Arbitration Rules", "ICC Rules"]
  }
}
```

This allows agents to evaluate legal compatibility during discovery — before any transaction begins.

**Task-level legal context:**

Before agents collaborate on a task via A2A, the initiating agent can include LCP references in the task metadata, establishing the legal framework governing the collaboration:

```json
{
  "task": {
    "id": "task-123",
    "metadata": {
      "legalContext": {
        "type": "sha256",
        "value": "0x7f83b165..."
      }
    }
  }
}
```

**Skill-level terms:** Each agent skill can declare required LCP terms, enabling agents to negotiate legal context as part of capability negotiation rather than as an afterthought.

#### MCP (Model Context Protocol)

MCP is the universal standard for agent-to-tool connectivity (97M+ monthly downloads), governed by the AAIF under the Linux Foundation. See Section 9 for detailed guidance on LCP as an MCP server.

**Tool-level legal context:** MCP tools that involve legally significant actions (purchases, commitments, agreements) can signal this through their standard annotations and description. The `destructiveHint` and `openWorldHint` annotations indicate state-changing external interactions; the tool description should specify that legal context verification is expected before invocation:

```json
{
  "name": "execute_purchase",
  "description": "Execute a purchase. Caller should verify legal context (LCP) before invocation.",
  "annotations": {
    "destructiveHint": true,
    "openWorldHint": true
  }
}
```

#### AP2 (Agent Payments Protocol)

AP2 is an open protocol (Apache 2.0) created by Google for secure AI-agent-driven payments. It uses W3C Verifiable Digital Credentials (VDCs) implemented as SD-JWT with Key Binding. 100+ partners including Mastercard, PayPal, American Express, and Coinbase.

AP2 defines three mandate types: Cart Mandates (human-present, user signs exact cart), Intent Mandates (human-not-present, user delegates within constraints), and Payment Mandates (for the payments ecosystem). Cart Mandates include a merchant cryptographic signature guaranteeing fulfillment and refund conditions.

**LCP alongside mandates:**

AP2 mandates capture *what was authorized* — the user approved this cart or delegated this intent. LCP captures *what terms govern the authorization* — what the merchant offered, what dispute resolution applies, what obligations extend beyond payment. These are complementary:

```
AP2 Cart Mandate: "User approved purchase of items X, Y, Z for $500"
LCP reference:    "Terms governing this purchase are at hash 0x7f83...,
                   jurisdiction NY, AAA arbitration, 30-day return policy"
```

The LCP reference SHOULD travel alongside the mandate — either in the A2A transport metadata layer or in an AP2 extension field. When the mandate and the LCP reference are both present, the combination creates a complete record: who authorized what, under what terms.

**Intent Mandate enrichment:** For autonomous (human-not-present) mandates, the natural language intent can be paired with machine-readable LCP constraints specifying the legal framework within which the agent may act. This extends the agent's authorization from financial constraints (spending caps, merchant categories) to legal constraints (acceptable jurisdictions, required dispute resolution methods, maximum contract duration).

**Dispute evidence integration:** AP2 defines a dispute evidence framework with liability allocation tables for scenarios including first-party fraud, agent mispicks, merchant non-fulfillment, and account takeover. The LCP `contentHash` and agreement record provide additional evidence: what terms were in effect, whether the merchant's offer matched the terms at transaction time, and what dispute resolution process was specified.

#### Mastercard Agent Pay and Verifiable Intent

Mastercard Agent Pay is the acceptance framework for agent-initiated transactions on the Mastercard network. It includes Know Your Agent (KYA) registration, agentic tokens (dynamic, cryptographically secure payment credentials via network-level tokenization), and the Dynamic Token Verification Code (DTVC) enabling no-code merchant integration through standard card payment fields, verified at the CDN layer via Cloudflare's Web Bot Auth.

Mastercard's Verifiable Intent is an open-source cryptographic framework (Apache 2.0, verifiableintent.dev) co-developed with Google. It creates a tamper-resistant record of consumer authorization using a three-layer SD-JWT credential format:

- **Layer 1 (Identity):** Issuer-signed credential binding consumer identity to a payment instrument (~1 year lifetime)
- **Layer 2 (Intent):** User-signed authorization with constraints — amount bounds, merchant categories, validity windows, geographic scope (~15 minutes lifetime in immediate mode; 24 hours to 30 days in autonomous mode)
- **Layer 3 (Action, autonomous mode only):** Agent-signed execution record showing what the agent actually did (~5 minutes lifetime)

Verifiable Intent uses Selective Disclosure to share only the minimum information each party needs: merchants see authorization validity, issuers see full transaction history, dispute systems see whether the transaction fell within or outside the mandate parameters.

**LCP as the merchant-side complement:**

Verifiable Intent captures the consumer's authorization chain — what the consumer authorized and whether the agent stayed within scope. LCP captures the merchant's terms — what was offered, under what conditions, with what obligations. Together they form a complete picture:

| What | Protocol |
|------|----------|
| Consumer authorized this agent | Verifiable Intent Layer 1-2 |
| Agent stayed within constraints | Verifiable Intent Layer 2-3 |
| Merchant offered these terms | LCP (`contentHash`) |
| Both parties agreed | LCP Level 3+ signed acceptance record |
| Dispute resolution is available | LCP Level 4 (`disputeResolution`) + AAA |

**Integration point — Verifiable Intent Layer 2:**

The consumer's Intent credential (Layer 2) defines financial constraints. LCP can extend this with legal constraints — acceptable terms of service, required dispute resolution, jurisdiction preferences. These legal constraints would be included in the Layer 2 credential alongside the existing financial constraints, signed by the user's device key, and carried through the mandate chain.

**Dispute resolution pipeline:** Verifiable Intent explicitly designs for dispute evidence but explicitly excludes the dispute mechanism itself. LCP Level 4 provides the mechanism: the `disputeResolution` field specifies the process (e.g., AAA Commercial Arbitration Rules), and the `api` field provides the entry point for filing. The combined evidence package — Verifiable Intent credential chain (consumer authorization) + LCP terms record (merchant offer) + LCP signed acceptance record (mutual consent) — provides a complete evidentiary foundation for arbitration.

---

## 8. Relationship to Authorization Protocols

*This section is advisory.*

The agentic commerce ecosystem has developed sophisticated authorization protocols that capture the **consumer's side** of a transaction — who authorized it, what constraints were set, and whether the agent complied. LCP captures the **merchant's side** — what terms were offered, what obligations were accepted, and what recourse is available. Together they form a complete agreement.

### 8.1 The Two Sides of a Transaction

| Side | What It Captures | Who Provides It |
|------|-----------------|----------------|
| Consumer authorization | Who authorized the agent, what constraints were set, whether the agent complied | Visa TAP, Mastercard Verifiable Intent, AP2 mandates |
| Merchant terms | What was offered, under what conditions, with what obligations and recourse | LCP |
| Mutual agreement | That both sides accepted, bound together with parties, jurisdiction, and timestamp | LCP Level 3+ (signed acceptance) |

Authorization protocols answer: "Is this agent legitimate and authorized?" LCP answers: "What terms govern this transaction?" Signed acceptance (Level 3+) binds the answers together into a verifiable record of mutual consent.

### 8.2 Complementary, Not Competing

LCP does not replace or duplicate authorization protocols. The relationship is additive:

- **Visa TAP** proves agent identity + consumer identity → **LCP** adds what terms the merchant offered
- **Mastercard Verifiable Intent** proves consumer authorization + agent compliance → **LCP** adds what the merchant committed to
- **AP2 mandates** prove user approval of a specific cart or intent → **LCP** adds the legal framework governing the transaction

No authorization protocol captures the merchant's terms, the mutual agreement, the dispute resolution process, or the temporal obligations that extend beyond payment. These are the domain of LCP.

### 8.3 Combined Evidence for Dispute Resolution

When a dispute arises, the resolution process requires evidence from both sides:

| Evidence | Source |
|----------|--------|
| Did the consumer authorize this transaction? | Verifiable Intent Layer 1-2 / TAP Consumer Recognition / AP2 Cart Mandate |
| Did the agent stay within authorized scope? | Verifiable Intent Layer 2-3 / AP2 mandate vs. transaction comparison |
| What terms did the merchant offer? | LCP `contentHash` + preserved terms document |
| Did both parties accept? | LCP signed acceptance record (Level 3-4) |
| What dispute resolution was specified? | LCP `disputeResolution` field |
| What jurisdiction governs? | LCP `disputeResolution.jurisdiction` |

No single protocol provides all of this evidence. The combination of authorization protocols + LCP creates the complete evidentiary foundation that institutional dispute resolution (AAA-ICDR) requires.

---

## 9. MCP as Delivery Mechanism

*This section is advisory.*

The Model Context Protocol (MCP) is the universal standard for agent-to-tool connectivity, with 97M+ monthly SDK downloads and support from every major AI platform (Claude, ChatGPT, Gemini, Copilot, Cursor, and others). MCP is governed by the Agentic AI Foundation (AAIF) under the Linux Foundation.

MCP's architecture is specifically designed to be extended through new servers. An LCP MCP server is the natural delivery mechanism for making legal context discoverable and accessible to every agent in the ecosystem.

### 9.1 LCP as MCP Tools

An LCP MCP server exposes legal context operations as callable tools:

| Tool | Description | Input |
|------|-------------|-------|
| `get_legal_context` | Fetch the LCP legal-context.json for a domain | `{ domain: string }` |
| `verify_terms` | Verify that a terms document matches its published hash | `{ termsUrl: string, expectedHash: string }` |
| `accept_terms` | Record cryptographic acceptance of specific terms | `{ agreementId: string, termsHash: string, signature: string }` |
| `create_agreement` | Create an agreement identity record binding parties, terms, and jurisdiction | `{ parties: Party[], termsUrl: string, jurisdiction: string }` |
| `get_agreement` | Retrieve an agreement identity record by ID | `{ agreementId: string }` |
| `initiate_dispute` | File a dispute with evidence against an agreement | `{ agreementId: string, evidence: Evidence[], claim: string }` |
| `get_dispute_status` | Check the status of an active dispute | `{ disputeId: string }` |

### 9.2 LCP as MCP Resources

Legal context data exposed as readable resources:

| Resource URI | Content |
|-------------|---------|
| `integra://legal-context/{domain}` | LCP legal-context.json for a domain |
| `integra://agreement/{id}` | Full agreement identity record |
| `integra://terms/{hash}` | Terms document content |
| `integra://dispute/{id}` | Dispute record and status |

### 9.3 LCP as MCP Prompts

Guided workflows for complex legal context operations:

| Prompt | Purpose |
|--------|---------|
| `review_terms` | Guided workflow for an agent to review, evaluate, and decide on terms before acceptance |
| `dispute_evidence_assembly` | Structured workflow for assembling dispute evidence from transaction records |

### 9.4 Integration Flow

```
1. Agent discovers LCP MCP server during initialization
2. Before any transaction, agent calls get_legal_context
   or reads integra://legal-context/{domain}
3. Agent evaluates terms against its principal's policy
4. If terms acceptable: agent calls accept_terms (Level 3)
5. Transaction proceeds through commerce protocol (ACP, UCP, MPP, etc.)
6. Agreement identity created via create_agreement (Level 4)
7. If dispute arises: agent calls initiate_dispute with evidence
```

This integration is protocol-agnostic. The same LCP MCP server works regardless of which commerce protocol the agent uses for the transaction. The agent accesses legal context through MCP and executes the transaction through ACP, UCP, MPP, x402, or any other protocol.

### 9.5 Deployment

An LCP MCP server can be deployed on any MCP-compatible hosting platform, including Cloudflare Workers (via McpAgent or createMcpHandler), AWS Lambda, or any HTTP server supporting the Streamable HTTP transport. The server is accessible to any MCP client — Claude, ChatGPT, Gemini, Copilot, and others — without per-platform integration.

---

## 10. IANA Considerations

This specification requests the registration of a well-known URI per [RFC 8615]:

| Field | Value |
|-------|-------|
| URI suffix | `legal-context.json` |
| Change controller | Integra Ledger |
| Specification document | This document |
| Status | Provisional |
| Related information | Provides legal context discovery for agentic commerce. Complements `/.well-known/ucp` (UCP), `/.well-known/agent-card.json` (A2A), and `/.well-known/acp.json` (ACP). |

---

## 11. Security Considerations

### 11.1 Transport Security

The discovery document and the terms document MUST be served over HTTPS. The TLS certificate provides domain identity anchoring — the same trust model as every other `/.well-known` file.

### 11.2 Document Integrity

At Level 2+, the `contentHash` provides integrity verification. Any party can download the terms document, compute SHA-256, and compare to the `contentHash`. A mismatch indicates the document has been altered.

At Level 1, there is no integrity verification mechanism. The agent relies on the TLS-secured connection for transport integrity but has no proof the document has not changed over time.

### 11.3 Terms Versioning

When vendors update their terms:
- The terms document at the URL changes
- The `contentHash` in `legal-context.json` is updated (Level 2+)
- Previous transactions reference the previous `contentHash` — the agent's saved copy and the receipt hash identify the version that was in effect

The `contentHash` in a transaction receipt is authoritative for that transaction. If an agent transacted with `contentHash` H1 and the vendor later updates to H2, the transaction is governed by H1 regardless.

### 11.4 Ephemeral Link Security

Ephemeral links (Section 5.1) SHOULD use unguessable URLs (e.g., containing a cryptographic random token) and SHOULD expire after a short period (minutes, not hours). The ephemeral link MUST be served over HTTPS.

### 11.5 Privacy

The `legal-context.json` file is publicly accessible. Vendors SHOULD NOT include sensitive information in this file. Contact information, dispute processes, and API endpoints in `legal-context.json` are visible to anyone who fetches the file.

For confidential terms, use the ephemeral link pattern (Section 5.1) or encrypted storage (Section 5.2) rather than publishing the terms URL in `legal-context.json`.

### 11.6 Rate Limiting

Implementations SHOULD implement rate limiting on the `/.well-known/legal-context.json` endpoint and on any API referenced by the `api` field. Public endpoints are susceptible to enumeration and abuse.

---

## 12. References

### Normative References

- [RFC 2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.
- [RFC 8174] Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, May 2017.
- [RFC 8615] Nottingham, M., "Well-Known Uniform Resource Identifiers (URIs)", RFC 8615, May 2019.

### Informative References

- [RFC 3161] Adams, C., et al., "Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP)", RFC 3161, August 2001.
- [RFC 7800] Jones, M., Bradley, J., and Tschofenig, H., "Proof-of-Possession Key Semantics for JSON Web Tokens (JWTs)", RFC 7800, April 2016.
- [RFC 9421] Backman, A., et al., "HTTP Message Signatures", RFC 9421, February 2024.
- [RFC 9457] Nottingham, M., Wilde, E., and S. Dalal, "Problem Details for HTTP APIs", RFC 9457, July 2023.
- Fisher, D. and McCormack, B., "Identity, Trust, and the Legal Foundations of Agentic Commerce", March 2026.
- Stripe and Tempo Labs, "Machine Payments Protocol", IETF Internet-Draft, 2026.
- OpenAI and Stripe, "Agentic Commerce Protocol", v2026-01-30.
- Google, "Universal Commerce Protocol", v1.0, January 2026.
- Google, "Agent Payments Protocol (AP2)", v0.1, September 2025.
- Google, "Agent-to-Agent Protocol (A2A)", v1.0, 2025. (Donated to Linux Foundation June 2025; v1.0 released subsequently.)
- Anthropic, "Model Context Protocol", spec version 2025-11-25.
- Visa, "Trusted Agent Protocol", 2025.
- Mastercard and Google, "Verifiable Intent", v0.1, March 2026.
- Cloudflare, "Web Bot Auth", draft-meunier-web-bot-auth-architecture, 2025.
- Coinbase and Cloudflare, "x402 Protocol", 2025.
- [EIP-712] Bloemen, R., Logvinov, L., and Evans, J., "Typed structured data hashing and signing", Ethereum Improvement Proposal 712.

---

## Appendix A: Relationship to Reference Implementations

This standard defines the discovery mechanism and document convention. How a service implements the legal infrastructure behind `legal-context.json` is not specified by this standard.

**Integra** provides one reference implementation featuring:
- On-chain existence proofs and agreement records (IntegraExistence, IntegraRecord)
- Composable resolver contracts (dispute resolution, escrow, compliance, identity, returns)
- Server-side middleware for zero-latency integration with MPP and other protocols
- IPFS document preservation via Pinata
- EIP-712 typed data schemas for signed acceptance
- MCP server exposing LCP tools, resources, and prompts (see Section 9)

Other implementations are possible and encouraged. The standard defines the interface; implementations provide the capability. The `api` field in `legal-context.json` is the hook from the standard to any implementation.

## Appendix B: Comparison to Existing Protocol Standards

| Feature | LCP | MPP | ACP | UCP | x402 | AP2 | TAP | Agent Pay | Verifiable Intent | A2A | MCP |
|---------|-----|-----|-----|-----|------|-----|-----|-----------|-------------------|-----|-----|
| Terms discovery | **Yes** | No | No | URLs only | No | No | No | No | No | No | No |
| Terms format signaling | **Yes** | No | No | No | No | No | No | No | No | No | No |
| Terms identified by hash | **Level 2+** | No | No | No | No | No | No | No | No | No | No |
| Explicit acceptance | **Level 3** | No | No | Partial | No | No | No | No | No | No | No |
| Dispute resolution clause (verifiable) | **Level 2+** | No | No | No | No | No | No | No | No | No | No |
| Dispute resolution service catalog | **Level 4** | No | No | No | No | Partial | No | No | No | No | No |
| Payment processing | No | Yes | Yes | Yes | Yes | Yes | Via Visa | Via MC | No | No | No |
| Checkout lifecycle | No | No | Yes | Yes | No | No | No | No | No | No | No |
| Agent identity | No | No | Partial | Partial | No | Partial | **Yes** | **Yes** | No | Partial | No |
| Consumer authorization | No | No | No | Partial | No | **Yes** | **Yes** | **Yes** | **Yes** | No | No |
| Agent-to-agent communication | No | No | No | No | No | No | No | No | No | **Yes** | No |
| Agent-to-tool connectivity | No | No | No | No | No | No | No | No | No | No | **Yes** |

LCP is complementary to all of these protocols. It provides the legal context layer — terms discovery, verification, signed acceptance, and dispute resolution hooks — that every other protocol defers. The authorization protocols (TAP, Agent Pay, Verifiable Intent, AP2) provide the consumer side; LCP provides the merchant side. Together they form a complete agreement. See Section 7 for per-protocol integration patterns and Section 8 for the relationship to authorization protocols.
