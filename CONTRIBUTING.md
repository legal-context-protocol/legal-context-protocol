# Contributing to the Legal Context Protocol

Thank you for your interest in contributing. We welcome improvements, bug fixes, and new ideas. Please read these guidelines to help maintain a high-quality, consistent, and collaborative project.

---

## Contributor License Agreement (CLA)

**All contributors must sign a Contributor License Agreement (CLA) before their contributions can be accepted.**

### For Individual Contributors

When you submit your first pull request:

1. The **CLA Assistant bot** will automatically comment on your PR
2. Click the link to review the [Individual CLA](legal/cla/INDIVIDUAL.md)
3. Click "I Agree" to sign electronically
4. Your signature is recorded for all future contributions

This takes less than one minute and only needs to be done once.

### For Corporate Contributors

If you are contributing on behalf of your employer:

1. Your employer must sign the [Corporate CLA](legal/cla/CORPORATE.md)
2. Follow the [Corporate CLA Process](legal/cla/CORPORATE_PROCESS.md)
3. Once approved, authorized employees can contribute without individual CLA signatures

Check with your employer about their IP policies before contributing.

---

## Branching Model

- **main**: The stable, released branch. All production-ready content lives here.
- **Feature branches**: For new features, fixes, or documentation updates. Create from `main` with descriptive names (e.g., `feature/add-webhook-support`, `fix/typo-in-schema`).
- **Pull Requests**: All changes must be submitted via PR. Never commit directly to `main`.

---

## Pull Request Guidelines

- **Scope**: Keep PRs focused and minimal. Separate unrelated changes.
- **Description**: Clearly describe what changed and why.
- **Review**: At least two TSC member approvals are required before merging. For PRs within a DWG's domain, one DWG member approval counts toward the two required.
- **CLA**: Ensure your CLA is signed (the bot will check automatically).
- **Linked Issues**: Reference any related issues in the PR description.

---

## Types of Changes

### Major Changes (Require SEPs)

Substantial changes to the protocol specification. Examples:

- Adding or removing fields in `legal-context.json`
- Changes to the well-known URI convention
- Modifications to the content hashing specification
- New protocol integration patterns

See [SEP Guidelines](docs/sep-guidelines.md) for the full process.

### Process Changes (Require SEPs)

Adjustments to governance, decision-making rules, contributor processes, or other structural revisions.

### Minor Changes (Do Not Require SEPs)

Documentation fixes, editorial clarifications, simple bugfixes, tooling improvements, example updates. These follow the standard PR process with two approvals.

---

## Dispute Resolution

Any disputes arising out of or relating to contributions to the Legal Context Protocol, including disputes regarding intellectual property rights, contributor agreements, or governance decisions, shall be resolved by arbitration administered by the American Arbitration Association-International Centre for Dispute Resolution in accordance with its Commercial Arbitration Rules. The place of arbitration shall be New York, NY. This agreement to arbitrate shall be governed by the Federal Arbitration Act, 9 U.S.C. 1-16.

---

## Code of Conduct

All participants are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful and constructive. Assume good intent. Report unacceptable behavior to the Founding Maintainers.

---

## Getting Help

- **Questions:** Open a [GitHub Discussion](https://github.com/legal-context-protocol/legal-context-protocol/discussions)
- **Bugs:** Create an issue
- **Feature proposals:** Start with a GitHub Discussion, then submit a SEP if appropriate
- **CLA questions:** See [Corporate CLA Process](legal/cla/CORPORATE_PROCESS.md)

---

## Project Governance

LCP is governed by Integra Ledger and the American Arbitration Association-International Centre for Dispute Resolution (AAA-ICDR) as Founding Maintainers. Learn more:

- [Governance Model](GOVERNANCE.md)
- [SEP Guidelines](docs/sep-guidelines.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

---

Thank you for helping make the Legal Context Protocol better.
