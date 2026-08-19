# Aggregate audit: `Academic_Phrasebank_Sections.xlsx`

**Audit date:** 2026-08-19
**Mode:** local, read-only, aggregate output only
**Release decision:** source file and wording excluded; zero candidates promoted

The workbook was supplied for academic use with a no-distribution/no-reproduction
restriction. This report intentionally contains no cell value, category label, phrase,
example, screenshot, style sample, or reversible fingerprint. The file was not changed
or copied into a public directory. This is a technical audit, not legal advice.

## Workbook structure

| Measure | Result |
| --- | ---: |
| Worksheets | 1 (`Sheet1`) |
| Used range | `A1:D24` |
| Physical rows / columns | 24 / 4 |
| Non-empty rows | 23 |
| Non-empty cells | 86 |
| Formulas | 0 |
| Excel tables / drawings | 0 / 0 |
| Logical blocks | 2 |
| Title / header / data / spacer rows | 2 / 2 / 19 / 1 |
| Payload/category cells | 19 |
| Category split | 6 section-level + 13 general = 19 |

All 86 non-empty cells were included in the style scan. Seven used-range style
signatures were present. Payload cells used two internally consistent signatures, one
per logical block; no within-block style deviation or unwrapped multiline payload was
detected. Style consistency does not imply redistribution clearance.

## Why two unit counts appear

The workbook uses two delimiter conventions. Counts from different tokenizers must not
be merged.

| View | Rule | Result |
| --- | --- | ---: |
| Structural cross-check | Each non-empty newline-delimited unit remains whole | 73 units |
| Migration parser | Split newlines, then literal space-slash-space delimiters | 120 candidates |

The first block contributes 60 newline units. The second contributes 13 newline units,
but 13 cells contain 47 literal slash delimiters; combined splitting yields 60 units in
that block. Total combined candidates: 120. This reconciles the views without exposing
source text.

## Duplicate analysis

For the 120-candidate migration view:

- 119 exact-unique values;
- one exact duplicate group, one extra occurrence, two affected candidates;
- the duplicate crosses a category boundary;
- NFKC, quote/dash folding, whitespace collapse, and case folding produce the same
  119/one-group result.

For the conservative 73-unit view, exact, normalised, punctuation-insensitive proxy,
and cross-category checks found zero duplicate groups. This is not a contradiction:
slash-separated sub-units remain combined in that view. Semantic near-duplicate
classification was not treated as release clearance; all source candidates remain
unresolved regardless of similarity score.

## Formatting and template signals

The following are aggregate diagnostics, not excerpts:

- 118 of 120 combined candidates contain an ASCII or Unicode ellipsis; 117 end in one.
- Two combined candidates use Unicode ellipsis typography.
- On the 73-unit structural view, nine space-before-punctuation signals were found;
  missing-space-after-punctuation and repeated non-ellipsis punctuation signals were
  zero.
- All 73 structural units start with an uppercase character; lowercase/non-letter starts
  were zero.
- One structural unit contains fewer than three words; one exceeds 250 characters.
- Uppercase single-letter slot signals occur in 14 structural units; parenthesised
  variant signals in four; 17 use mixed placeholder/variant conventions.
- Square, curly, angle-bracket, underscore, and slash-style placeholder signals were
  not detected as placeholder syntaxes. Slash remains a delimiter in the second block.
- Unmatched round/square/curly/angle delimiters, unmatched double quotes, blank internal
  lines, control characters, NBSPs, tabs, and missing-space-after-punctuation signals
  were all zero in the structural checks.

Ellipses and single letters are presentation conventions, not a formal typed-slot
schema. They would require original redrafting and explicit placeholder conversion;
mechanical substitution would not establish originality.

## Lexical risk triage

A narrow, case-insensitive aggregate scan ran across the 120 parsed candidates. It used
generic word/stem triggers and printed counts only. Buckets overlap and do not establish
meaning, error, or safety.

| Signal | Candidate count | Interpretation |
| --- | ---: | --- |
| British-spelling trigger | 2 | Variant metadata needed; no automatic conversion |
| American-spelling trigger | 0 | Narrow list only; not proof of absence |
| Strong causal-language trigger | 4 | Requires study-design and claim review |
| Association-language trigger | 1 | Must not be upgraded to causation |
| Statistical-significance trigger | 3 | Needs estimate/context review |
| Absolute/proof-language trigger | 3 | Needs certainty/evidence review |
| Novelty trigger | 0 | Narrow list only; unsupported novelty still prohibited |
| Genericity trigger | 5 | May be adaptable or may be underspecified |

Potentially misleading, ambiguous, incomplete, or over-generic wording cannot be
reliably decided from a keyword hit. No item-level judgement is published because that
would require reproducing or characterising restricted wording. Every such property is
therefore **unresolved for migration**, and no candidate passes the evidence-safety
gate.

## Taxonomy signals

The 19 primary categories contain 1–10 conservative units (mean 3.8421; median 1;
coefficient of variation 1.0888; Gini 0.5061). Thirteen categories are singletons or
contain at most three units. The largest 20% of categories hold 54.79% of units.

Under the 120-candidate migration delimiter, category sizes are 4–10 (mean 6.3158;
median 5; zero singletons). This second shape describes split candidates, not a different
workbook. Both views are retained so delimiter choice remains auditable.

No normalised category-label collision, uncategorised payload, or hierarchy-marker
category was detected. A secondary-label field follows a 15/2/2 distribution. The two
blocks use different header schemas.

These figures show an imbalanced, flat seed organisation—not a release taxonomy.
RhetoriLex builds its hierarchical semantic taxonomy independently and does not promote
the workbook's labels.

## Audit conclusions

1. Workbook mechanics are simple: one sheet, no formulas or embedded objects.
2. Delimiter choice materially changes unit counts; parser methods must be named.
3. Source presentation conventions are not canonical templates or typed slots.
4. Keyword signals require human evidence/methods review and cannot establish safe use.
5. Rights and provenance remain unresolved for every source-derived unit.
6. Public migration eligibility is therefore **0 of 120**.

See `migration-report.md`, `../PROVENANCE.md`, and
`../data/sources/source-registry.yaml` for the clean-room decision.
