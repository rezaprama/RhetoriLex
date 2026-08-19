# Provenance and clean-room policy

RhetoriLex is built as an original editorial system. External sources may inform
research questions, taxonomy design, or validation, but source wording enters no
release unless its rights, attribution, transformation, and review status are
explicitly cleared.

This document records engineering policy, not legal advice. Copyright scope depends
on jurisdiction and facts. When rights remain uncertain, RhetoriLex excludes the
material.

## Release invariant

Every canonical entry must be traceable to an accepted contribution and must declare:

- stable semantic ID and version;
- `method: original_editorial`;
- `source_reuse: false`;
- contributor/reviewer identity or review record;
- claim strength, evidence requirement, and causal status;
- editorial status and any risk flags.

Release validation fails when provenance is missing, unresolved, incompatible, or
contradictory. High-level similarity to a communicative function is not permission to
reuse source expression.

## Source classes

| Class | Permitted role | Public output |
| --- | --- | --- |
| Original editorial contribution | Canonical template candidate after review | Accepted template plus metadata |
| Open corpus approved in source registry | Frequency, distribution, and naturalness analysis | Aggregates and independently written abstractions only |
| Restricted or unclear source | Rights review and exclusion testing | Bibliographic facts and aggregate audit facts only |
| User manuscript | In-memory operation explicitly requested by user | User-requested result only; never corpus data |

No external corpus is fetched merely because a URL exists in the registry. An
ingestion change needs a dedicated license decision, pinned version, checksum,
attribution plan, minimisation plan, and reviewer approval.

## Clean-room workflow

1. Define rhetorical function and evidence constraints without consulting a restricted
   phrase inventory.
2. Draft a template from general linguistic competence or a contributor's own words.
3. Record protected semantic slots, claim strength, and unsafe use cases.
4. Scan for exact and near overlap against the release dataset and any legally held
   exclusion set. Comparison does not authorize source publication.
5. Review naturalness, usefulness, evidence calibration, originality, and provenance.
6. Accept, revise, reject, or deprecate through a review record. Never silently delete
   a stable released ID.

Restricted source text must remain outside Git, logs, fixtures, screenshots, issues,
pull requests, CI artifacts, prompts, and generated reports. Tests should use synthetic
examples written for this project.

## Initial workbook decision

The supplied spreadsheet carried an academic-use-only/no-redistribution notice.
RhetoriLex performed a local, read-only aggregate audit. Two parser views were used to
understand structure; neither output wording publicly. All source-derived candidates
remain provenance-unresolved and **zero were promoted**. The workbook itself, raw cell
values, category wording, and staging records are excluded from the repository.

See `reports/xlsx-audit.md` and `reports/migration-report.md` for aggregate results.
The final release set also passed the aggregate exclusion check in
`reports/overlap-exclusion.md`: no exact/skeleton match and no sequence or token match
at the documented 0.80 thresholds. This exclusion test supports review but does not
prove copyright status or independent creation.

## Named external sources

- **Manchester Academic Phrasebank:** conceptual orientation and citation only; phrase
  inventory excluded. See the [about page](https://www.phrasebank.manchester.ac.uk/about-academic-phrasebank/)
  and [copyright notice](https://www.manchester.ac.uk/copyright/).
- **Elsevier OA CC-BY Corpus v3:** potential future aggregate-only research source under
  separate review; not ingested. Dataset DOI:
  [10.17632/zm33cdndxs.3](https://doi.org/10.17632/zm33cdndxs.3).
- **BAWE:** excluded from the pipeline. Its archive record states CC BY-NC-SA 3.0.

Current structured decisions live in `data/sources/source-registry.yaml`.

## Research foundation

These sources orient original model design; no prose, examples, inventories, or data
from them are incorporated:

- genre and move analysis: [10.1017/CBO9781139524827](https://doi.org/10.1017/CBO9781139524827),
  [10.1017/S0261444808005235](https://doi.org/10.1017/S0261444808005235), and
  [10.1017/9781009030199](https://doi.org/10.1017/9781009030199);
- corpus phraseology and disciplinary variation:
  [10.1075/scl.28](https://doi.org/10.1075/scl.28),
  [10.1016/j.jeap.2019.01.003](https://doi.org/10.1016/j.jeap.2019.01.003), and
  [10.1075/scl.95.06gra](https://doi.org/10.1075/scl.95.06gra);
- stance and reader interaction:
  [10.1177/1461445605050365](https://doi.org/10.1177/1461445605050365).

Responsible paraphrasing and attribution requirements were checked against primary
guidance from the [US Office of Research Integrity](https://ori.hhs.gov/28-guidelines-glance-avoiding-plagiarism),
[Harvard Guide to Using Sources](https://usingsources.fas.harvard.edu/what-constitutes-plagiarism-0),
[Harvard's avoidance guidance](https://usingsources.fas.harvard.edu/how-avoid-plagiarism),
[UNESCO](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research),
[Elsevier](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals),
and [ICMJE](https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html).
These references do not replace a user's institutional or publisher rules.

## License mapping

- software, scripts, configuration, tests, and Agent Skill code: Apache-2.0;
- original canonical data, synthetic benchmarks, reports, and documentation:
  CC-BY-4.0;
- third-party material: its own license, if ever accepted and clearly marked;
- restricted local inputs: no RhetoriLex license and no distribution.

`REUSE.toml` supplies file-level machine-readable mappings. License decisions reference
the [Apache text](https://www.apache.org/licenses/LICENSE-2.0.html),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), and
[REUSE Specification](https://reuse.software/spec/). The
[WIPO copyright FAQ](https://www.wipo.int/en/web/copyright/faq-copyright) is background,
not a jurisdiction-specific opinion.

## Reporting a concern

Report provenance, attribution, or rights concerns privately using the process in
`SECURITY.md`. Include the affected file/ID, the claimed source, a canonical URL, and
why overlap may be protectable. Maintainers may quarantine an entry immediately while
review proceeds. Removal is risk control, not an admission of infringement.
