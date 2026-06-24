# Security Policy

The Legal Context Protocol (LCP) is a specification. "Security" here covers two
things:

- Weaknesses in the specification text — ambiguities or designs that would lead
  conforming implementations into an insecure state.
- Vulnerabilities in the reference materials published in this repository (the
  JSON Schema and examples).

Section 12 of the specification (Security Considerations) describes the threat
model the standard is designed to address.

## Reporting a Vulnerability

Please report suspected security issues privately. Do not open a public issue for
a suspected vulnerability.

- **Preferred:** use GitHub's private vulnerability reporting — the **Security**
  tab → **Report a vulnerability** — on this repository.
- If that is unavailable, contact a maintainer through the channels listed in
  [CONTRIBUTING.md](CONTRIBUTING.md).

Please include the affected section or file, a description of the issue, the
impact you foresee, and any suggested remediation.

## What to Expect

- Acknowledgement within five business days.
- Confirmed issues are handled as errata or, where they change normative
  behavior, through the SEP process (see [GOVERNANCE.md](GOVERNANCE.md) and
  [docs/sep-guidelines.md](docs/sep-guidelines.md)).
- We will coordinate disclosure timing with the reporter.

## Scope

In scope: the specification text, the JSON Schema, and the examples in this
repository.

Out of scope: third-party implementations of LCP, which are the responsibility of
their respective authors.
