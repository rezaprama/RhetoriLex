# Restricted-source overlap exclusion check

**Date:** 2026-08-19
**Mode:** local, read-only, aggregate output only
**Decision:** no release entry crossed the exclusion thresholds

This check compared 48 public canonical templates with 120 locally parsed workbook segments in memory. It did not print or persist workbook text, labels, cell locations, nearest-neighbour pairs, or private candidates.

## Results

| Check | Result |
| --- | ---: |
| Exact normalised template or slot-stripped skeleton matches | 0 |
| Slot-stripped `SequenceMatcher` ratio at least 0.80 | 0 |
| Token Jaccard similarity at least 0.80 | 0 |
| Maximum sequence ratio | 0.7907 |
| Maximum token Jaccard similarity | 0.5556 |
| Source text emitted | No |

Normalisation used lowercase ASCII word tokens. The skeleton view removed named public template slots before comparison. The test is deliberately conservative and only excludes likely overlap; it does not prove copyright status, independent creation, naturalness, or permission.

The catalog's separate release basis remains original editorial authorship, required `source_reuse: false` provenance, and zero promotion from the workbook. The workbook stays ignored and absent from release artifacts.

See `xlsx-audit.md`, `migration-report.md`, and `../PROVENANCE.md`.
