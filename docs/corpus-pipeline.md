# Corpus pipeline policy

RhetoriLex v0.1 ships no external corpus and has no automatic corpus downloader. This document defines the gate for future aggregate-only validation work.

## Deny by default

A source registry entry is not ingestion permission. Before any download or processing, a pull request must provide:

1. canonical source URL, named creators, version, publication date, and license;
2. pinned files and cryptographic checksums;
3. an attribution and notices plan;
4. allowed and prohibited transformations;
5. a minimisation plan that keeps source text out of logs and artifacts;
6. a leakage test and reviewer;
7. a deletion and incident-response path;
8. explicit maintainer approval.

## Permitted output shape

Approved analysis should prefer non-reconstructive aggregates such as counts, normalised frequencies, broad disciplinary distributions, and validation metrics. It must not publish source sentences, phrase inventories, contiguous excerpts, or metadata that makes source expression reconstructable.

External text must never become a canonical template automatically. An independently authored pattern needs its own provenance, semantic slots, evidence contract, originality review, and stable ID.

## Isolation

Raw corpora belong outside the repository in a user-selected private directory. A pipeline must require explicit input and output paths, reject paths inside tracked release directories, and avoid printing text samples. CI should use synthetic fixtures only.

## Initial source decisions

- Supervisor workbook: excluded; local aggregate audit only; zero promotions.
- Manchester Academic Phrasebank: excluded from ingestion; conceptual citation only.
- BAWE: excluded by project policy.
- Elsevier OA CC-BY Corpus v3: possible future aggregate-only research after a separate gate; not ingested.

Normative records are in `data/sources/source-registry.yaml` and `PROVENANCE.md`.
