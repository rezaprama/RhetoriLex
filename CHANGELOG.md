# Changelog

All notable project changes are recorded here. RhetoriLex follows
[Semantic Versioning](https://semver.org/) for software. Dataset snapshots may carry a
separate calendar-based version in release notes.

## [Unreleased]

### Planned

- Expand original reviewed rhetorical coverage.
- Add frozen retrieval and evidence-preservation benchmarks.
- Evaluate corpus-derived aggregate signals only after source approval.

## [0.1.0] — 2026-08-19

### Added

- Initial offline Python catalog, search, filtering, suggestions, and CLI surface.
- Original evidence-aware starter catalog, taxonomy, and claim-strength contract.
- Compact `rhetorilex` Agent Skill with progressive-disclosure references.
- Schema/data validation, synthetic evaluation cases, and deterministic checks.
- Static documentation/explorer and contributor-facing project documentation.
- Aggregate XLSX audit and clean-room migration decision with zero source promotion.
- Source registry, provenance policy, third-party notices, and REUSE license mapping.
- Governance, conduct, security, contribution, citation, and six-month roadmap files.

### Security and integrity

- Core retrieval operates locally without an API key.
- Restricted workbook, private staging data, source corpora, and manuscript content are
  excluded from version control and release artifacts.
- Canonical entries require original-editorial provenance and explicit evidence/claim
  metadata.

[Unreleased]: https://github.com/rezaprama/RhetoriLex/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/rezaprama/RhetoriLex/releases/tag/v0.1.0
