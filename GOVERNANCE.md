# Legal Context Protocol (LCP) Governance

## Overview

The **Legal Context Protocol (LCP)** is an open standard for discovering the legal context of agentic commerce transactions. LCP's governance is designed to ensure clear decision-making, transparent evolution of the specification, and a stable foundation for long-term stewardship as the protocol matures.

---

## Shared Principles

LCP exists to promote open, discoverable, and verifiable legal context for agentic commerce. All TSC members, including the Founding Maintainers, commit to upholding the following principles. These serve as the foundation for all governance decisions and the basis under which the Founding Maintainers' veto authority may be exercised as a last resort.

1. **Mission Protection:** Decisions must not materially undermine LCP's core mission of making legal context discoverable, verifiable, and actionable in agentic commerce.

2. **Neutrality Protection:** Decisions must not privilege a specific vendor, platform, payment provider, or dispute resolution institution in a way that harms neutrality.

3. **Security and Integrity:** Changes must not introduce systemic security risks or compromise the integrity guarantees (ATR hashing, clause verification) that the protocol provides.

4. **Protocol Integrity:** Changes must not fracture the standard or create incompatible forks.

5. **Simplicity:** The normative core must remain minimal. One well-known URI, one required field. Complexity belongs in advisory guidance and extensions, not in the standard itself.

6. **Considered Decision-Making:** Particularly contentious decisions need more time to develop and gain community consensus, even if they may pass the TSC.

---

## The Technical Steering Committee (TSC)

The TSC is the decision-making authority for the protocol's evolution, specification maintenance, and technical integrity.

### Composition and Structure

The TSC has up to 7 seats. Each seat is held by one organization, including Integra Ledger and the American Arbitration Association-International Centre for Dispute Resolution (AAA-ICDR).

Seats are filled incrementally as qualified contributors emerge.

### Membership Criteria

TSC seats are appointed by the Founding Maintainers based on the following criteria:

1. **Shared Vision:** A demonstrated commitment to advancing discoverable legal context in agentic commerce. Candidates must align with LCP's mission and long-term direction.

2. **Contributions:** A visible track record of meaningful contributions to the LCP repository. This includes authoring or co-authoring merged Pull Requests, proposing Specification Enhancement Proposals (SEPs), actively participating in discussions, or contributing reference implementations, integrations, or adoption documentation.

3. **Time Commitment:** Members are expected to dedicate a few hours per week to TSC responsibilities and to actively engage in regular meetings.

The TSC reviews membership quarterly.

### Joining the TSC

Organizations interested in joining the TSC should reach out to anyone from the TSC or Founding Maintainers for more details on the process.

### Member Expectations

- Dedicate a few hours weekly to the review of Pull Requests and SEPs.
- Actively participate in regular TSC meetings.
- Drive discussions and provide technical guidance across official community channels (GitHub, Discord).
- Guide and support Domain Working Groups (DWGs) where relevant.

### Strategic Value of Membership

- Direct influence on the standard governing how legal context is discovered and verified in agentic commerce.
- Member organization logos featured on the LCP website and official documentation.
- Members may formally use the title: "Member of the LCP Technical Steering Committee."
- Regular collaboration alongside technical and legal leads from the LCP ecosystem.

### Current TSC Members

| Seat | Organization | Representative(s) |
|------|-------------|-------------------|
| 1    | Integra Ledger | David Fisher |
| 2    | AAA-ICDR | TBD |

---

## Domain Working Groups (DWGs)

Domain Working Groups are community-driven groups focused on adapting and extending LCP for specific industry verticals or technical domains.

### Envisioned Domains

The following domains reflect the stakeholder landscape for legal context in agentic commerce. DWGs are not created at launch — they are formed when contributors self-organize around a domain.

- **Commerce Protocols** — Integration with MPP, ACP, x402, UCP, and other agentic commerce protocols.
- **Dispute Resolution** — ADR providers (AAA, JAMS, ICC), clause standardization, content-addressed clause registries, and machine-readable service catalogs.
- **Financial Services** — Institutional contracting, ISDA integration, structured dispute resolution frameworks, and Merkle DAG contract architectures.
- **Cloud & Platform Services** — SLAs, multi-service terms, enterprise agreement frameworks, and platform legal architecture.
- **Identity & Authorization** — Interaction with Visa TAP, Mastercard Verifiable Intent, AP2 mandates, and agent authorization chains.

### Formation

DWGs operate outside the core TSC but require formal recognition to carry governance weight. Any group of contributors may self-organize around a domain, but to be recognized as an official DWG they must:

- Include members from at least two distinct organizations.
- Submit a proposal to the TSC outlining the group's scope, goals, and initial membership.

The TSC votes to approve or reject the proposal by simple majority.

### Autonomy

Once officially recognized, a DWG operates with a high degree of autonomy. Each group defines its own cadence, operating norms, and the specific problems it aims to address. Leadership within the group is self-organizing.

### Relationship to the TSC

- DWGs are expected to surface new features or changes back to the TSC as SEPs, which follow the standard SEP review and voting process.
- For standard PRs within a DWG's domain, one approval from a recognized DWG member counts toward the two approvals required for merging.

### Strategic Value of DWG Membership

- Shape how LCP is applied within your industry, ensuring the standard meets real-world needs.
- Establish your organization as a recognized domain authority within the LCP ecosystem.
- DWG member organizations are listed on the LCP website under their respective working group.
- Gain direct input into SEPs that affect your vertical before they reach the broader TSC vote.

---

## The Technical Review Process

### Standard Pull Requests (Non-SEP)

Merging requires two approvals from TSC members. For PRs within a DWG's domain, one DWG member approval counts toward the two required.

### Specification Enhancement Proposals (SEPs)

SEPs are the mechanism for proposing significant changes to the LCP specification. All SEPs are decided by a vote of the TSC.

The SEP lifecycle:

1. **Sponsorship:** Every SEP must be sponsored by a TSC member to proceed. The sponsor is responsible for shepherding the proposal through the review process.

2. **Community Review:** Once sponsored, a mandatory 7-business-day public review window is opened for feedback and technical scrutiny. This review period must span across at least one instance of the regular TSC meeting.

3. **TSC Meeting:** The TSC holds a regular meeting dedicated to discussing, debating, and voting on pending SEPs. Members who cannot attend may express their votes or feedback asynchronously before or after the meeting.

4. **Voting:** SEPs are adopted or rejected by a simple majority vote (50%+1) of the TSC.

### Types of Changes

1. **Major Changes (Require SEPs):** Any substantial, complex, or controversial change to the protocol. Examples: adding or removing fields in `legal-context.json`, changes to the well-known URI convention, modifications to the ATR hashing specification, new protocol integration patterns.

2. **Process Changes (Require SEPs):** Adjustments to governance, decision-making rules, contributor processes, or other structural revisions.

3. **Minor Changes (Do Not Require SEPs):** Documentation fixes, editorial clarifications, simple bugfixes, tooling improvements, example updates. These may be merged following the standard PR process with two approvals.

---

## The Founding Maintainers

Integra Ledger and AAA-ICDR are the Founding Maintainers of LCP. Their role is to steward the early growth of the protocol and its governance structures.

### Why These Two Organizations

LCP exists at the intersection of technology and law. Integra Ledger brings the technology — smart contracts, content-addressed document systems, and agentic commerce infrastructure. AAA-ICDR brings the legal authority — the world's largest and most recognized dispute resolution institution, with institutional credibility that no technology company can replicate. Together they represent both sides of the protocol's mission: making legal context discoverable (technology) and making it meaningful (institutional credibility).

### Responsibilities

- Appoint and remove TSC members based on the published membership criteria.
- Ensure the protocol's long-term coherence, security, and alignment with its founding mission.
- Each holds one seat on the TSC with the same voting rights as any other member.

### Governance Evolution

The Founding Maintainers' appointment authority is intended as a transitional mechanism for the protocol's early stages. As the TSC matures and the contributor base grows, this structure is expected to evolve toward broader participation and shared ownership of governance decisions.

### Founding Maintainers' Reserve Authority

In order to safeguard the core principles of LCP — including neutrality, openness, and the integrity of the standard — the Founding Maintainers reserve a limited veto authority over TSC decisions. This authority exists solely to protect the protocol from outcomes that could compromise its foundational mission. This veto is expected to be exercised in extremely rare situations and is not intended for day-to-day governance. Any exercise of this authority will be accompanied by a clear, written explanation shared with the full TSC.

The veto can only be used to **block** a change, never to override the TSC and force one through. If the Founding Maintainers want to see a change adopted, they advocate for it through the same TSC process as everyone else.

A veto does not kill a proposal permanently. It pauses the change and sends it back to the TSC for further discussion. The proposal author and sponsor are welcome to revise and resubmit.

The veto applies only to SEPs. It does not apply to routine operational decisions, standard PRs, DWG formation, or day-to-day governance matters.

---

## Contributor License Agreement (CLA)

All contributors must sign a Contributor License Agreement before their contributions can be accepted.

### For Individual Contributors

When you submit your first pull request, the CLA Assistant bot will automatically prompt you to review and sign the Individual CLA. This takes less than one minute and only needs to be done once.

### For Corporate Contributors

If you are contributing on behalf of your employer, your employer must sign the Corporate CLA. The process involves creating a GitHub Issue with the signed agreement, maintainer review, and confirmation. See the CLA documentation for details.

### Why a CLA Is Required

The CLA clarifies intellectual property rights and protects both contributors and users of the protocol. Contributors retain ownership of their work. The CLA grants the project perpetual, worldwide, royalty-free rights to use and redistribute contributions under the Apache 2.0 License.

---

## Future Evolution and Neutral Governance

The Founding Maintainers recognize the long-term goal of transitioning LCP governance to a neutral foundation. A full transition will be undertaken when:

- A healthy and active community has developed, demonstrating consistent participation and collaboration.
- LCP achieves broad adoption across independent stakeholders — commerce protocols, payment networks, dispute resolution providers, cloud platforms, and enterprises.
- Sufficient community and institutional participation exists to sustain multi-party governance.
- Legal and structural frameworks are in place to ensure neutrality and continuity.

The transition may involve hosting under an established foundation (such as the Linux Foundation or OASIS) or establishing a standalone foundation, depending on the ecosystem's needs at the time of transition.

---

## Frequently Asked Questions

**Q: Is there a cost or fee associated with joining the TSC or a DWG?**

A: No. There are no membership fees. Participation in the TSC and DWGs is earned through contributions and commitment, not financial investment.

**Q: Can TSC members or contributors participate in competing or complementary protocols?**

A: Yes. There are no restrictions against working with other protocols. Participants remain free to engage with any protocol simultaneously.

**Q: Does the TSC only have room for large, well-known companies?**

A: No. Seats are earned through contributions and commitment. Smaller organizations making strong contributions will be considered. Outside the TSC, Domain Working Groups provide meaningful leadership opportunities for any contributor.

**Q: Can a TSC member lose their seat?**

A: Yes. Membership is reviewed quarterly. If a member organization is no longer meeting expectations — not engaging in meetings, not reviewing PRs or SEPs, not actively contributing — the TSC will first reach out and ask the organization to re-commit. If engagement does not improve, the TSC may revisit their seat. Members may also step down voluntarily.

**Q: Can anyone start a Domain Working Group?**

A: Yes. Any group of contributors can self-organize around a domain. To be officially recognized, the group must include members from at least two distinct organizations and submit a proposal to the TSC for approval.

**Q: What behavior is not allowed within LCP governance?**

A: LCP governance is built on mutual respect and fair play. The following are not permitted:

- Using LCP channels or governance forums for product marketing or self-promotion.
- Pushing the direction of the protocol to disproportionately favor any single member or organization.
- Blocking or stalling proposals to disadvantage a competitor.
- Using a TSC or DWG seat to gain unfair competitive intelligence.
- Misrepresenting LCP affiliation or governance roles for commercial advantage.

All participants are expected to engage in good faith, with the shared goal of advancing the standard for the benefit of the entire ecosystem.

**Q: Under what circumstances would the Founding Maintainers use their veto?**

A: The veto is a last resort, reserved for situations that threaten the foundational principles of the protocol. Examples: a decision that materially undermines LCP's core mission, a change that privileges a specific vendor at the expense of neutrality, a change that introduces systemic security risks, a change that fractures the standard into incompatible forks, or a particularly contentious decision that needs more time and broader consensus.

**Q: Can the veto be used to push through a change the TSC has rejected?**

A: No. The veto can only block a change, never force one through.

**Q: What does a veto scenario look like in practice?**

A: For illustrative purposes: imagine the TSC adopts a change requiring all LCP implementations to depend on a proprietary API controlled by a single company. This would compromise the neutrality of the protocol and could be vetoed. Or suppose a specification change replaces the open `atrHash` mechanism with a closed, vendor-specific verification system — that is a systemic integrity risk worth blocking. These are extreme scenarios, and the expectation is that most concerns like these would be resolved through normal TSC discussion well before a veto is ever considered.

**Q: Can an organization hold a seat on both the TSC and a DWG?**

A: Yes. TSC membership and DWG participation are independent. An organization on the TSC can also have representatives active in one or more DWGs. This is encouraged — it helps ensure alignment between core governance and domain-specific work.

**Q: Who represents an organization on the TSC — is it always the same person?**

A: Each organization holds one seat, but the individual representing that organization may change. It is up to the member organization to designate their representative. We ask that organizations maintain consistency where possible so that context and relationships are preserved, but understand that personnel changes happen.

**Q: What happens if the TSC can't reach a majority on a SEP?**

A: Every SEP is decided by a simple majority vote. If a proposal does not pass by (50%+1) vote, the author and sponsor are welcome to revise it based on the feedback and resubmit.

**Q: Can someone contribute to LCP without being on the TSC or a DWG?**

A: Absolutely. LCP is an open standard and anyone can contribute by opening Pull Requests, proposing SEPs, participating in discussions, or building implementations. The TSC and DWGs are governance structures for decision-making, not gatekeepers of contribution.

---

## Dispute Resolution

Any controversy or claim arising out of or relating to participation in the Legal Context Protocol project, including disputes regarding intellectual property rights, contributor agreements, or governance decisions, shall be settled by arbitration administered by the American Arbitration Association-International Centre for Dispute Resolution in accordance with its Commercial Arbitration Rules and judgment on the award rendered by the arbitrator(s) may be entered in any court having jurisdiction thereof. The place of arbitration shall be New York, NY. This agreement to arbitrate shall be governed by the Federal Arbitration Act, 9 U.S.C. 1-16.

---

## License

The Legal Context Protocol specification and all contributions are licensed under the [Apache License 2.0](LICENSE).
