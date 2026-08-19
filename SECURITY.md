# Security policy

## Supported versions

RhetoriLex is pre-1.0 software. Security fixes target the latest release and `main`.
Older alpha versions may receive guidance but are not guaranteed patches. The release
notes will identify any exception.

## Private reporting

Use GitHub's **Report a vulnerability** / private security advisory feature for:

- code execution, path traversal, unsafe archive/document parsing, or injection;
- dependency or release-pipeline compromise;
- leakage of manuscripts, credentials, restricted corpora, or private staging data;
- a committed secret or a way to make core operations transmit text unexpectedly;
- a provenance failure that would require sharing protected source text to explain.

Do not open a public issue, paste live secrets, or upload the restricted workbook.
Include affected version/commit, impact, reproduction steps using synthetic data, and
the least sensitive evidence sufficient to investigate. If private reporting is not
enabled, contact the repository owner through the private contact method on their
GitHub profile and request a secure channel.

For ordinary wording quality, taxonomy, or non-sensitive academic-integrity bugs, use
a normal issue.

## Response targets

Maintainers aim to acknowledge a complete report within three business days, provide
an initial assessment within ten business days, and coordinate disclosure after a fix
or mitigation exists. These are targets, not guarantees. Severity, maintainer capacity,
and upstream coordination can change timing.

Reports will be handled on a need-to-know basis. A reporter acting in good faith should
avoid privacy violations, service disruption, social engineering, destructive testing,
and access beyond what proves the issue.

## Security design commitments

- Offline core search requires no credential or external service.
- User manuscripts are not sent to external services by default.
- Data files are treated as untrusted input and never executed.
- Corpus ingestion is opt-in, version-pinned, provenance-gated, and isolated from
  canonical release output.
- CI and release workflows use least-privilege permissions.
- Secrets, raw restricted data, and private staging artifacts are ignored and must not
  enter logs or fixtures.

Optional integrations must document provider, data sent, retention assumptions, user
configuration, and a local/off switch before release.

## Advisories and credit

Validated vulnerabilities receive a GitHub security advisory when appropriate.
Reporter credit is offered with consent. Maintainers may withhold exploit detail until
users can update and may quarantine data immediately during provenance review.

This policy does not create a bug bounty or legal safe-harbour agreement.
