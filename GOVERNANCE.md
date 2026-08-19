# Governance

RhetoriLex uses transparent maintainer-led governance with strong provenance and
evidence-safety gates. User utility matters; scientific meaning, privacy, and source
rights take priority over growth or phrase count.

## Roles

- **Contributor:** submits issues, code, data, review, or documentation.
- **Reviewer:** provides repeatable technical, linguistic, methods, accessibility, or
  provenance review. Review authority applies only to demonstrated scope.
- **Maintainer:** merges changes, manages releases, enforces community/security policy,
  and appoints reviewers or maintainers.

Reza Prama is the initial maintainer. Maintainer status is earned through sustained,
high-quality contributions, sound judgement, respectful review, and reliable handling
of provenance and security. Appointment is recorded publicly in the repository.

## Decisions

Routine, reversible changes use lazy consensus: a reviewed pull request may merge when
tests pass, applicable owners approve, and no unresolved blocking concern remains.

Open a design issue or RFC before:

- breaking a public API, stable ID, schema, or claim-strength contract;
- approving or changing use of an external corpus;
- adding a networked or manuscript-processing integration;
- changing project licenses, governance, or release criteria;
- adding a major dependency or persistent service.

An RFC states the problem, evidence, alternatives, privacy/provenance effects,
compatibility plan, and decision deadline. Maintainers seek consensus. If disagreement
remains, the lead maintainer records a decision and rationale. Decisions may be
revisited when new evidence appears.

## Non-negotiable gates

Any maintainer may block release material that has unresolved provenance, incompatible
rights, manuscript leakage, fabricated evidence, silent claim strengthening, or a
credible security/privacy risk. A block identifies the failed gate and evidence needed
to clear it. It is not a veto over unrelated preferences.

Canonical entries need editorial and evidence-safety review. External source ingestion
also needs a separate license/provenance approval. Passing automated tests does not
replace these reviews.

## Releases

Maintainers cut semantic software releases and separately version data snapshots.
Release notes list data additions, changed taxonomy, deprecations/replacements,
benchmark changes, security fixes, and provenance decisions. Stable IDs are deprecated,
not silently reassigned or removed.

At least one maintainer verifies tests, deterministic artifacts, license mapping, source
registry, and changelog. High-risk releases should receive independent review when the
community has a qualified reviewer.

## Conflicts and recusals

Reviewers disclose financial, institutional, authorship, or source-ownership conflicts
that could reasonably affect judgement. A conflicted maintainer does not make the sole
decision on a contested source, conduct report, or commercial integration. If no
unconflicted maintainer exists, pause the decision and seek an external qualified
reviewer.

## Security and conduct

Sensitive reports follow `SECURITY.md`; community reports follow
`CODE_OF_CONDUCT.md`. Urgent protective actions may be private. Public summaries should
preserve privacy and restricted content while explaining policy changes.

## Succession and inactivity

A maintainer may step down at any time. After 90 days without response to documented
release/security needs, active maintainers may transfer operational ownership through
a public decision record. If only one maintainer exists, they should nominate at least
one recovery contact before a stable 1.0 release. Repository ownership must never be
sold as a shortcut around community or provenance obligations.

Governance changes require an RFC, a public review period of at least 14 days, and a
recorded maintainer decision. License changes additionally require contributor-rights
analysis; no governance vote can relicense third-party material.
