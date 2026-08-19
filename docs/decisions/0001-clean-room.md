# ADR 0001: Original clean-room catalog

- Status: accepted
- Date: 2026-08-19
- Decision owners: RhetoriLex maintainers

## Context

The project needs useful academic rhetorical patterns while supporting broad public use. The supplied workbook has an academic-use and no-redistribution notice. Several well-known phrase and corpus resources have distinct copyright or license conditions. Editing or mass-paraphrasing restricted expression would not create a dependable rights boundary.

## Decision

RhetoriLex releases only independently authored editorial patterns. Canonical entries must declare `method: original_editorial` and `source_reuse: false`. Restricted inventories may inform exclusion checks or non-expressive aggregate QA when access permits, but their wording, labels, ordering, examples, and formatting do not enter public artifacts.

The supplied workbook remains ignored and local. Its audit reports contain aggregate structure only. All migration candidates are unresolved and zero are eligible for promotion.

External corpora are deny-by-default. Even an openly licensed corpus does not feed templates automatically; it requires a separate documented gate and independently authored output.

## Consequences

Benefits:

- clear editorial provenance;
- compatible public and commercial use of original releases;
- lower source-leakage and patchwriting risk;
- stronger evidence metadata than a plain phrase list.

Costs:

- slower catalog growth;
- manual drafting and review;
- fewer patterns in the initial release;
- no claim that the catalog reproduces the coverage of an established resource.

## Rejected alternatives

- Copy workbook cells into a public dataset.
- Rewrite each workbook phrase with synonyms.
- Scrape or mirror a phrase inventory.
- Mix noncommercial/share-alike corpus text into CC-BY output.
- Let a model promote corpus sentences directly into canonical data.

## Review trigger

Revisit only if source owners provide suitable written permission or if a new, clearly compatible source and leakage-safe method passes governance review. Existing released patterns still require their own provenance.
