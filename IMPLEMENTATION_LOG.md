# Implementation log

This append-only record captures material engineering and editorial decisions. It is
not a substitute for commits, release notes, or the source registry.

## 2026-08-19 — Repository bootstrap

- Established Python 3.10+ package architecture with dependency-light offline core.
- Selected stable semantic identifiers, explicit placeholder metadata, and immutable
  catalog entries as initial data contracts.
- Added lexical/fuzzy retrieval and filters that treat rhetorical function and evidence
  compatibility as first-class metadata.
- Kept optional AI/network integration outside the core path.

## 2026-08-19 — Evidence and claim safety

- Defined an ordered claim-strength/evidence contract and causal-design guard.
- Required evidence-like slots where a template makes an evidence-bearing move.
- Required `original_editorial` / `source_reuse: false` provenance for release entries.
- Chose synthetic test language for meaning-preservation and routing evaluation.

## 2026-08-19 — Restricted workbook audit

- Read `Academic_Phrasebank_Sections.xlsx` locally without modifying it.
- Recorded structure and parser counts only; no phrase or category wording entered a
  tracked artifact.
- Reconciled two parsing views: conservative newline units and migration delimiter
  units. Their counts remain separate in `reports/xlsx-audit.md`.
- Applied supplied academic-use/no-redistribution notice. Marked every derived candidate
  unresolved and promoted zero candidates. Kept workbook and private staging ignored.
- Ran the aggregate restricted-source exclusion check across 48 public templates and
  120 private segments: zero exact/skeleton matches and zero SequenceMatcher or token
  Jaccard matches at the 0.80 exclusion thresholds. See
  `reports/overlap-exclusion.md`; no source text was emitted.

## 2026-08-19 — External-source review

- Restricted Manchester Academic Phrasebank to conceptual orientation/citation; no
  inventory ingestion, scraping, mirroring, or transformation.
- Recorded Elsevier OA CC-BY Corpus v3 as a possible future aggregate-only research
  source; did not ingest it.
- Excluded BAWE from the RhetoriLex pipeline because its CC BY-NC-SA terms do not fit
  the project's intended distribution workflow.
- Centralised decisions in `data/sources/source-registry.yaml` and established a
  deny-by-default ingestion gate.

## 2026-08-19 — Licensing and governance

- Applied Apache-2.0 to software and Agent Skill code.
- Applied CC-BY-4.0 to original data, reports, benchmarks, and documentation.
- Added official license texts and `REUSE.toml` file-level mappings.
- Added contribution, conduct, security, governance, citation, provenance, third-party
  notice, changelog, and roadmap documents.
- Recorded that licensing documentation is project policy and not legal advice.

## 2026-08-19 — Release readiness rule

- Defined initial release as blocked by failed tests, nondeterministic artifacts,
  unresolved provenance, restricted source leakage, broken offline quick start, or an
  unmitigated high-severity security/evidence-safety defect.
- Kept community-growth targets subordinate to measured utility and integrity.
