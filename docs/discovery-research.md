# Discovery research

- **Snapshot:** 2026-08-19
- **GitHub capture:** 2026-08-19T12:11:05Z
- **Status:** descriptive research, not market-size or demand evidence

RhetoriLex uses discovery research to choose accurate public language, repository topics,
and testable outreach hypotheses. It does not use popularity data to change claim-safety
rules or to copy another project's content.

## Research question

Which terms describe RhetoriLex accurately, appear in the surrounding GitHub ecosystem,
and preserve its specific value: evidence-calibrated rhetorical moves for humans and AI
agents?

Three evidence lanes were considered:

1. GitHub topic counts as a repository-supply signal;
2. GitHub keyword result counts as an index-coverage signal;
3. Google Trends as a possible relative-interest signal.

Only the first two produced reproducible measurements. Google Trends direct measurement
was unavailable in this environment, so no search volume or proxy value is reported.

## Measurement method

GitHub observations came from the official REST
[repository search endpoint](https://docs.github.com/en/rest/search/search#search-repositories).
Each query used `per_page=1`; only `total_count` and `incomplete_results` were retained.
All recorded searches returned `incomplete_results: false`. GitHub search remains a
changing index with query and result limitations, so counts are point-in-time facts.

Repository metadata came from the official
[get-a-repository endpoint](https://docs.github.com/en/rest/repos/repos#get-a-repository).
GitHub's [watching documentation](https://docs.github.com/en/rest/activity/watching#about-watching)
states that `subscribers_count` is the number of watchers, while legacy `watchers`,
`watchers_count`, and `stargazers_count` all represent stars. RhetoriLex reports watchers
from `subscribers_count` only.

The complete dated records, including source, geo, language, window, metric, value,
`retrieved_at`, confidence, query, and notes, are in
[`data/discovery/discovery-signals-2026-08-19.json`](../data/discovery/discovery-signals-2026-08-19.json).
The stable machine-readable keyword deliverable is
[`data/discovery/keyword-research.json`](../data/discovery/keyword-research.json); every
record uses the required `keyword`, `source`, `geography`, `language`, `time_window`,
`metric`, `value`, `retrieved_at`, `confidence`, and `notes` fields.

## GitHub topic signals

| Topic query | Repository matches |
| --- | ---: |
| `topic:agent-skills` | 16,343 |
| `topic:research-tools` | 1,121 |
| `topic:academic-writing` | 1,004 |
| `topic:literature-review` | 879 |
| `topic:scientific-writing` | 243 |
| `topic:rhetoric` | 36 |
| `topic:research-writing` | 31 |

These values describe maintainer-assigned repository topics. They do not measure people,
searches, downloads, demand, impact, correctness, or quality. A smaller topic can be
underused vocabulary rather than an underserved market.

## GitHub keyword signals

Queries searched repository name, description, and README fields.

| Exact query core | Repository matches |
| --- | ---: |
| `"academic writing"` | 9,151 |
| `academic "agent skills"` | 7,258 |
| `"research writing"` | 5,988 |
| `"scientific writing"` | 3,437 |
| `phrasebank` | 1,381 |
| `codex "academic writing"` | 826 |
| `"academic english"` | 814 |
| `"claim strength" "academic writing"` | 70 |
| `"rhetorical moves" academic` | 49 |
| `"evidence calibrated" writing` | 45 |

These are GitHub repository-index result counts, **not keyword search volume**. Broad terms
have more repository coverage; narrower safety language has less coverage. This supports
using familiar category terms for discovery while explaining evidence calibration in the
value proposition. It does not prove user preference or conversion.

## Google Trends availability

| Source | Geo | Requested window | Metric | Value | Confidence |
| --- | --- | --- | --- | --- | --- |
| Google Trends | Worldwide | five years ending 2026-08-19 | relative search interest | unavailable (`null`) | unavailable |
| Google Trends | Indonesia | five years ending 2026-08-19 | relative search interest | unavailable (`null`) | unavailable |

The official Explore pages were attempted, but no reproducible export could be retrieved
in this environment. No browser display, third-party SEO estimate, or GitHub count was
substituted. `null` means unavailable, not zero. A future update may add Trends values
only with a saved official export, query terms, geo, window, category, retrieval time,
and normalization notes.

## Positioning decision

RhetoriLex should sit inside familiar categories—academic writing, scientific writing,
research tools, and agent skills—then differentiate with capabilities that are directly
verifiable in this repository:

- rhetorical function, not generic polish, is the retrieval unit;
- claim strength and evidence requirements are explicit metadata;
- causal wording has design guards;
- rewriting protects citations, quantities, negation, uncertainty, and population scope;
- core search and validation work offline and deterministically;
- released patterns are original editorial work under a clean-room policy;
- the same catalog serves writers, editors, reviewers, and AI-agent workflows.

Recommended GitHub About description:

> Open academic and scientific writing phrasebank, rhetorical moves, and evidence-safe research writing skills for papers, theses, literature reviews, and manuscripts.

Recommended topics:

`academic-writing`, `scientific-writing`, `research-writing`, `academic-english`,
`phrasebank`, `rhetorical-moves`, `literature-review`, `research-tools`, `agent-skills`,
`codex`, `evidence-based`, `python`.

Selection follows measured topic/keyword relevance plus verified product compatibility;
it does not turn repository counts into a demand claim.

Avoid unsupported copy such as “largest,” “best,” “most trusted,” “complete,” or
“proven demand.” The snapshot cannot substantiate those claims.

## Research basis

Discovery language is separate from the intellectual basis of the data model. Original
RhetoriLex design is oriented by published work on:

- genre and move analysis:
  [10.1017/CBO9781139524827](https://doi.org/10.1017/CBO9781139524827),
  [10.1017/S0261444808005235](https://doi.org/10.1017/S0261444808005235), and
  [10.1017/9781009030199](https://doi.org/10.1017/9781009030199);
- corpus phraseology and disciplinary variation:
  [10.1075/scl.28](https://doi.org/10.1075/scl.28),
  [10.1016/j.jeap.2019.01.003](https://doi.org/10.1016/j.jeap.2019.01.003), and
  [10.1075/scl.95.06gra](https://doi.org/10.1075/scl.95.06gra);
- stance and reader interaction:
  [10.1177/1461445605050365](https://doi.org/10.1177/1461445605050365).

These works inform questions and model structure; their prose, examples, inventories,
and datasets are not incorporated. See [`PROVENANCE.md`](../PROVENANCE.md).

## Discovery experiment plan

1. Keep the recommended About description and topics stable for one measurement cycle.
2. Capture GitHub traffic or referral data only from an authorized first-party source,
   with its time window and privacy limitations. Establish a baseline before setting a
   numeric target.
3. Record issue, discussion, and installation feedback by stated use case rather than
   treating stars as satisfaction.
4. Test README phrasing without changing safety contracts or inflating claims.
5. Refresh repository/search snapshots quarterly, preserving earlier snapshots instead
   of rewriting history.

## Release gates

| Gate | Pass condition |
| --- | --- |
| Measurement | Every number has source, query/metric, scope, and UTC retrieval time. |
| Availability | Missing measurements remain explicit `null`; no estimates are invented. |
| Interpretation | Repository counts are never described as search volume or demand. |
| Originality | No competing repository content is copied into data, docs, or Skill assets. |
| Positioning | Public claims map to checked-in behavior, tests, or metadata. |
| Localization | English and Indonesian READMEs communicate the same core claims and limits. |
| Refresh | Volatile metrics carry a snapshot date and are not presented as current forever. |

## Sources

- [GitHub repository search endpoint](https://docs.github.com/en/rest/search/search#search-repositories)
- [GitHub get-a-repository endpoint](https://docs.github.com/en/rest/repos/repos#get-a-repository)
- [GitHub watching versus starring](https://docs.github.com/en/rest/activity/watching#about-watching)
- [GitHub stars documentation](https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars)
- [Google Trends Explore, Worldwide query attempted](https://trends.google.com/trends/explore?date=today%205-y&q=academic%20writing,scientific%20writing)
- [Google Trends Explore, Indonesia query attempted](https://trends.google.com/trends/explore?date=today%205-y&geo=ID&q=academic%20writing,scientific%20writing)

Research captured on 2026-08-19. Metrics are descriptive snapshots, not endorsements.
