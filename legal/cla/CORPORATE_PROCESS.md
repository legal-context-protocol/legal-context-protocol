# Corporate CLA Process

This document explains the steps required for Corporate CLA signatories.

## For Organizations

### Step 1: Create a GitHub Issue

1. Go to the [LCP Issues page](https://github.com/legal-context-protocol/legal-context-protocol/issues)
2. Click "New Issue"
3. Title: `Corporate CLA: [Your Company Name]`
4. Copy the signature template from [CORPORATE.md](CORPORATE.md) into the issue body
5. Fill in all required information: corporation name, address, point of contact, email, date, Schedule A (authorized GitHub usernames), and the agreement statement
6. Add labels: `cla` and `corporate-cla`
7. Submit the issue

The GitHub issue serves as the electronic signature and legal record of the Corporate CLA execution.

### Step 2: Wait for Maintainer Review

- Monitor the GitHub issue for comments from maintainers
- Respond to any questions or requests for clarification
- Wait for the `cla-signed` label to be added

Expected timeline: within 5 business days.

### Step 3: Confirmation

- Maintainers will add the `cla-signed` label to your issue
- Your company will be added to [SIGNATORIES.md](SIGNATORIES.md)
- Your authorized contributors will be added to the CLA Assistant allowlist
- The issue will be closed (but remains accessible)

### Step 4: Updating Authorized Contributors (Ongoing)

When adding or removing authorized contributors:

1. Go to your company's original CLA issue (closed but you can still comment)
2. Add a comment with the updated Schedule A
3. Maintainers will update the allowlist and SIGNATORIES.md
4. Maintainers will confirm the update with a comment

You must update Schedule A when:
- A new employee will contribute to the project
- An employee leaves the company
- An employee changes roles and should no longer contribute
- Your Point of Contact changes

## Why Not Fully Automated?

Corporate CLAs require an authorized signatory to legally bind the corporation, explicit listing of authorized contributors, and human verification that the signer has authority. These cannot be automated while maintaining legal validity. This manual process is standard practice in open source — used by the Apache Software Foundation, Linux Foundation projects, and most major open-source projects with CLAs.

The manual effort is minimal: ~10 minutes to create the initial issue, ~2 minutes for Schedule A updates.

## Questions?

- Review [CORPORATE.md](CORPORATE.md) for the full CLA text
- Check [SIGNATORIES.md](SIGNATORIES.md) for examples
- Ask in [GitHub Discussions](https://github.com/legal-context-protocol/legal-context-protocol/discussions)
