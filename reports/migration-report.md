# Workbook migration report

**Run type:** audit-only dry run
**Input:** local `Academic_Phrasebank_Sections.xlsx`
**Date:** 2026-08-19
**Canonical entries created from input:** **0**

The objective was to test a migration shape without distributing the supplied workbook
or converting restricted wording into an ostensibly new dataset. Processing occurred
locally and emitted aggregate counts only. No raw or normalised source string, category
label, screenshot, candidate record, or private staging artifact was committed.

## Dry-run result

| Measure | Result |
| --- | ---: |
| Payload/category cells detected | 19 |
| Newline-only structural units | 73 |
| Combined newline + literal slash-delimited candidates | 120 |
| Exact unique candidates | 119 |
| Exact/normalised duplicate groups | 1 / 1 |
| Cross-category duplicate groups | 1 |
| Candidates with resolved redistribution provenance | 0 |
| Candidates promoted to canonical release | **0** |

The duplicate counts use the 120-candidate migration parser. The 73-unit structural
view is a cross-check and must not be used as its denominator. Full reconciliation and
quality signals appear in `xlsx-audit.md`.

A post-build clean-room scan found zero exact candidate matches in the public text tree
and zero normalised substring matches among source candidates of at least 20 characters.
The scan reported counts and paths only; it emitted no source wording.

## Pipeline disposition

| Proposed migration step | Dry-run disposition |
| --- | --- |
| Read workbook | Completed locally, read-only |
| Detect logical blocks and payload cells | Completed; aggregate counts retained |
| Split multi-unit cells | Completed in memory with named delimiter rule |
| Normalise whitespace/Unicode/punctuation for comparison | Completed for duplicate keys only |
| Preserve original wording | Not in public staging; source remained local and ignored |
| Create deterministic candidate IDs | No public IDs reserved for excluded source units |
| Classify into canonical taxonomy | Not promoted; source labels not reused |
| Add provisional metadata | Rights/provenance status remained unresolved |
| Run duplicate checks | Completed; aggregate result retained |
| Promote candidates | Rejected: 0 promoted |

The repository migration utility can create deterministic `private.*` identifiers and
quarantined source records only after an exact authorization marker is supplied and only
inside an explicitly named private root. It never promotes records. No such private
quarantine is a release dependency or public artifact.

Normalisation was used to compare values, not to manufacture originality. Punctuation,
case folding, slot substitution, synonym replacement, or sentence restructuring would
not by themselves clear source rights.

## Promotion gates

| Gate | Status | Reason |
| --- | --- | --- |
| Redistribution permission | Fail | No public permission compatible with repository distribution |
| Provenance resolution | Fail | Source-derived units remain unresolved |
| Independent authorship | Not established | Dry run intentionally did not redraft source wording |
| Restricted-source overlap | Not cleared | No source expression may enter release data |
| Schema/slot review | Not performed for promotion | Source conventions are not typed canonical slots |
| Claim/evidence safety | Not performed for promotion | Aggregate triggers cannot determine contextual safety |
| Editorial naturalness/usefulness | Not performed for promotion | Would require item-level restricted-text review |

Failure of the rights/provenance gate is sufficient to exclude every candidate. Later
technical or editorial quality cannot override that failure.

## Clean-room replacement

RhetoriLex replaces migration with an independent contribution path:

1. Define rhetorical intents from open scholarship at a conceptual level and from the
   project's own product requirements.
2. Draft original templates without viewing a restricted phrase inventory during
   composition.
3. Add typed slots, evidence requirements, claim strength, causal status, use/avoid
   notes, and risk metadata.
4. Record `method: original_editorial` and `source_reuse: false`.
5. Run exact/near-overlap checks as an exclusion gate; never publish the comparison set.
6. Require editorial and evidence-safety review before acceptance.

This process may cover the same abstract communicative function while avoiding reuse of
source expression, organisation, and labels. Restricted input does not determine the
canonical dataset.

## Reproducibility boundary

Public reports reproduce aggregate results but deliberately cannot reproduce source
wording. Maintainers with proper local authorization may repeat the audit against their
own copy. Release CI must succeed without the workbook; absence of private input is an
expected state, not an error.

The source decision is recorded in `../data/sources/source-registry.yaml`. Policy and
licensing context appear in `../PROVENANCE.md` and `../THIRD_PARTY_NOTICES.md`. This
report documents a conservative project decision and is not legal advice.
