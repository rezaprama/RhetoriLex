# Contributing to RhetoriLex

RhetoriLex welcomes code, rhetorical patterns, corrections, corpus evidence,
benchmarks, documentation, translations, and integrations. Small, reviewable changes
with explicit provenance are easiest to merge.

By submitting a contribution, you represent that you have the right to contribute it
and agree that accepted code/Skill contributions are provided under Apache-2.0 and
accepted original data/documentation contributions under CC-BY-4.0. Do not submit
confidential, restricted, assignment-only, paywalled, or copied material. This is a
project contribution policy, not legal advice.

## Fast path

1. Search existing issues and entries.
2. Open an issue first for taxonomy changes, new dependencies, external corpora,
   breaking schema changes, or more than ten phrase candidates.
3. Create a focused branch and add tests or validation evidence.
4. Run the checks documented in the README.
5. Open a pull request explaining purpose, provenance, risk, and user-visible change.

Use Python 3.10 or newer. Core retrieval must remain offline and dependency-light.
Never put manuscript text, secrets, corpus source sentences, or restricted workbook
content into fixtures or CI logs.

## Phrase proposal

One strong pattern is more useful than a bulk dump. A proposal should include:

```yaml
id: RLX-INT-999
function: interpret_evidence
title: Short human-readable label
template: "Given {finding}, one cautious interpretation is {interpretation}."
description: Explain the rhetorical work this original pattern performs
stage: discussion
disciplines: [general]
claim_strength: tentative
evidence_requirement: direct
causal_design_required: false
placeholders: [finding, interpretation]
keywords: [interpretation, caution]
notes: State when to use it and when not to use it
risk: medium
provenance:
  method: original_editorial
  author: RhetoriLex contributors
  source_reuse: false
version: 1
```

Adjust fields to the current schema. Also answer:

- What user intent does this serve?
- What evidence is minimally required?
- Could it imply causation, significance, novelty, certainty, or generalisability?
- Which numbers, citations, negation, scope, and uncertainty must remain protected?
- Did you write it independently? If a source informed the proposal, identify it and
  explain what was learned without reproducing source wording.
- What makes it distinct from existing entries?

Do not propose text by copying an academic phrasebank, article, thesis, reviewer
letter, user's manuscript, or generated bulk list. Generic language can still require
careful provenance. If uncertain, describe the function and let maintainers help draft
an original expression.

## External evidence or corpus contribution

No corpus enters a script or build until `data/sources/source-registry.yaml` records:

- canonical source and version;
- authors/organisation and access date;
- exact license and attribution terms;
- allowed and prohibited uses;
- redistribution decision;
- intended derived output and minimisation controls;
- checksum and reviewer when ingestion is approved.

A compatible-looking license is not automatic approval. Corpus PRs must keep raw text
outside Git and CI, produce deterministic aggregates, and demonstrate that source
sentences cannot leak into templates or artifacts.

## Code and tests

- Preserve public API compatibility or document a migration.
- Keep stable IDs stable; deprecate with a replacement instead of silently deleting.
- Add tests for schema validity, unique IDs, placeholder agreement, provenance, and
  retrieval behaviour when relevant.
- Rewriting changes need invariant cases for citations, numbers, signs, units, dates,
  population, negation, comparison direction, uncertainty, and causal status.
- Use synthetic examples. Never turn a third-party sentence into a fixture.
- Avoid network calls in core search and never transmit manuscript content by default.

## Documentation and translation

Write clear international English. Academic language should be precise, not inflated.
Translations should preserve meaning, safety warnings, links, and attribution. The
canonical phrasebank remains academic English; translated documentation does not
silently create translated canonical entries.

## Review gates

A maintainer may request domain or methods review. Canonical data needs all applicable
gates:

- schema and deterministic-build checks pass;
- provenance is resolved;
- wording is independently authored;
- evidence/claim contract passes;
- naturalness and rhetorical usefulness are reviewed;
- duplicate and similarity checks pass;
- risk notes and attribution are complete.

Licensing, privacy, security, or scientific-validity concerns can block a change even
when tests pass. See `GOVERNANCE.md` for decisions and `CODE_OF_CONDUCT.md` for community
standards.
