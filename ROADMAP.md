# Roadmap: August 2026 to February 2027

This is a six-month execution window measured from the August 2026 baseline to the
February 2027 review. Dates are targets, not promises. Quality gates outrank phrase
count, launch timing, and GitHub-star goals.

## Baseline — August 2026

**Goal:** publish a credible clean-room alpha.

- Ship original starter catalog, offline retrieval, Python API/CLI, and Agent Skill.
- Validate schema, placeholders, stable IDs, claim/evidence contract, and provenance.
- Publish aggregate-only workbook audit; promote zero restricted seed strings.
- Establish dual license mapping, source registry, governance, security, and CI.
- Provide quick start, evidence-safe examples, and static documentation baseline.

**Exit gate:** clean install; deterministic tests/builds; no unresolved provenance or
restricted file in Git/release; core usage needs no network or API key.

## Month 1 — September 2026

**Theme:** retrieval quality and contributor experience.

- Expand intent coverage through small, original, reviewed batches.
- Freeze initial retrieval benchmark and report Recall@K/MRR transparently.
- Add phrase-proposal, benchmark, and deprecation workflows.
- Improve explorer accessibility, mobile layout, and copy/paste ergonomics.
- Publish one concise tutorial showing intent → evidence → language.

**Exit gate:** every new entry passes provenance and claim-strength checks; benchmark
cases remain synthetic or clearly licensed.

## Month 2 — October 2026

**Theme:** evidence preservation.

- Broaden invariant tests for numbers, citations, uncertainty, scope, negation, units,
  population, comparison direction, and causal status.
- Add explanations for frequently confused reporting verbs and causal vocabulary.
- Benchmark risky observational, null, qualitative, and mixed-method prompts.
- Recruit methods and academic-writing reviewers through targeted, non-spam outreach.

**Exit gate:** no accepted rewrite path can silently strengthen a frozen test claim.

## Month 3 — November 2026

**Theme:** reproducible corpus-support experiment.

- Draft an RFC for Elsevier OA CC-BY Corpus v3; do not ingest before approval.
- If approved, pin version/checksum, isolate raw data, and generate aggregate-only
  frequency/section signals with attribution.
- Test source-sentence leakage and reject extractive template generation.
- Publish reproducible method, limitations, and negative results.

**Exit gate:** raw corpus text stays outside Git/CI/releases; outputs cannot reconstruct
source sentences; source registry and attribution remain complete.

## Month 4 — December 2026

**Theme:** discipline calibration and documentation reach.

- Pilot reviewed overlays for two contrasting disciplinary families.
- Measure where general patterns fail rather than claiming universal coverage.
- Add Indonesian README/docs translation, then invite Chinese, Japanese, and Spanish
  translation review as maintainers become available.
- Improve editor/agent integration examples without adding mandatory services.

**Exit gate:** overlays declare scope and evidence; translations preserve warnings and
do not create an unreviewed translated phrasebank.

## Month 5 — January 2027

**Theme:** beta hardening.

- Target v0.5 only if quality supports it; review stale and high-risk entries.
- Stabilise schema migration/deprecation tools and deterministic data exports.
- Add package, Skill, docs, and clean-environment installation smoke tests.
- Review accessibility, privacy data flows, dependency risk, and release recovery.

**Exit gate:** release candidate reproduces from source; deprecated IDs resolve to
documented replacements; no high-severity security/provenance issue remains open.

## Month 6 — February 2027

**Theme:** public evidence and sustainable community.

- Publish six-month benchmark/coverage report with methods and limitations.
- Decide next release milestone from evidence, not target phrase count.
- Present resources to writing centres, graduate communities, corpus/NLP researchers,
  and agent developers through useful demonstrations—never mass promotion.
- Review maintainer capacity, contributor retention, governance, and next six months.

**Exit gate:** public claims match measured results; roadmap review documents misses,
trade-offs, provenance decisions, and next priorities.

## Metrics

Primary: retrieval accuracy, intent coverage, invariant violations, provenance pass
rate, review latency, data quality, and reproducibility. Community: contributors,
merged external PRs, downstream uses, citations, downloads, and useful issue reports.
Reach metrics such as stars are observed but never bought, exchanged, automated, or
treated as evidence of scientific quality. A 5,000-star stretch objective is not a
forecast or release criterion.
