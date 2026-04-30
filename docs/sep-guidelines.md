# Specification Enhancement Proposal (SEP) Guidelines

## What Is a SEP?

A Specification Enhancement Proposal (SEP) is the mechanism for proposing significant changes to the Legal Context Protocol specification. SEPs ensure that major changes receive proper review, community feedback, and TSC deliberation before adoption.

## When Is a SEP Required?

### Major Changes (Require SEPs)

- Adding, modifying, or removing fields in `legal-context.json`
- Changes to the well-known URI convention
- Modifications to the ATR hashing specification
- New protocol integration patterns
- Breaking changes that are not backward-compatible
- Complex or controversial topics requiring community discussion

### Process Changes (Require SEPs)

- Adjustments to governance roles or responsibilities
- Changes to decision-making rules
- Modifications to contributor processes
- Structural revisions to the governance document

### Minor Changes (Do NOT Require SEPs)

- Documentation fixes or editorial clarifications
- Simple bugfixes
- Tooling improvements
- Example updates

When in doubt, ask a TSC member.

## SEP Lifecycle

### 1. Draft

Author writes the SEP as a Pull Request using the SEP proposal template. The PR should include:

- **Title:** Clear, descriptive title prefixed with `SEP:`
- **Motivation:** Why is this change needed?
- **Specification:** The proposed change in precise detail
- **Backward Compatibility:** How does this affect existing implementations?
- **Security Considerations:** Any security implications
- **Examples:** Before/after examples where applicable

### 2. Sponsorship

Every SEP must be sponsored by a TSC member to proceed. The sponsor:

- Reviews the proposal for completeness and clarity
- Ensures it aligns with LCP's shared principles
- Shepherds the proposal through the review process
- Presents it at the TSC meeting

Authors may reach out to any TSC member for sponsorship.

### 3. Community Review

Once sponsored, a mandatory **7-business-day** public review window opens. During this period:

- The PR is labeled `sep` and `under-review`
- Community members may comment with feedback, questions, and concerns
- The review period must span across at least one TSC meeting
- The author is expected to respond to substantive feedback

### 4. TSC Discussion

The SEP is discussed at the TSC meeting. The sponsor presents the proposal. TSC members debate merits, concerns, and alternatives. Members who cannot attend may express their positions asynchronously before or after the meeting.

### 5. Vote

SEPs are adopted or rejected by a **simple majority vote (50%+1)** of the TSC.

- If adopted: the PR is merged and the change takes effect
- If rejected: the author and sponsor may revise and resubmit based on feedback

### 6. Founding Maintainers' Reserve Authority

The Founding Maintainers may exercise their veto authority over an adopted SEP if it threatens the protocol's foundational principles. See [GOVERNANCE.md](../GOVERNANCE.md) for details. A veto pauses the change for further discussion — it does not permanently kill the proposal.

## SEP Template

```markdown
# SEP: [Title]

## Motivation

[Why is this change needed? What problem does it solve?]

## Specification

[The proposed change in precise detail. Include field definitions,
JSON examples, and normative requirements (MUST/SHOULD/MAY).]

## Backward Compatibility

[How does this affect existing implementations? Is it additive or breaking?]

## Security Considerations

[Any security implications of this change.]

## Examples

[Before/after examples showing the change in context.]

## References

[Links to related issues, discussions, or external specifications.]
```

## Tips for Successful SEPs

- **Start with a discussion.** Open a GitHub Issue or Discussion before writing the full SEP. Gauge interest and get early feedback.
- **Keep it focused.** One change per SEP. Don't bundle unrelated modifications.
- **Show your work.** Include concrete examples and use cases. Abstract proposals are harder to evaluate.
- **Address backward compatibility explicitly.** The most common concern with any change.
- **Be responsive during review.** The 7-day window is for active dialogue, not silence.
