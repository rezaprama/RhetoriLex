# GitHub landscape

- **Repository snapshot:** 2026-08-19T12:11:05Z
- **Recursive-tree snapshot:** 2026-08-19T12:16:17Z
- **Scope:** public GitHub metadata and commit-pinned file counts only

This landscape maps adjacent GitHub projects without importing their repository
content. Names, topics, activity dates, API license fields, and counts are factual
metadata. Categories and positioning notes are original RhetoriLex annotations.

## Method

Repository metrics were captured with GitHub's official REST
[get-a-repository endpoint](https://docs.github.com/en/rest/repos/repos#get-a-repository).
Stars, forks, open issues, topics, language, push time, and API-reported SPDX values are
point-in-time values. `NOASSERTION` or `null` in the API license field is not a legal
conclusion about repository contents.

GitHub explicitly documents that `subscribers_count` is watchers; legacy
`watchers_count` is the same concept as stars in REST responses. Tables below therefore
use `subscribers_count` for **Watchers**.

Skill-file footprint was measured separately with the official
[recursive Git Trees endpoint](https://docs.github.com/en/rest/git/trees#get-a-tree).
Each count is pinned to a default-branch commit, requires `truncated: false`, and counts
blob paths equal to `SKILL.md` or ending in `/SKILL.md`. It does not measure distinct
capabilities, validation, quality, users, or installations.

## Requested comparison set

| Repository | Stars | Forks | Watchers | Open issues | API license | Last push (UTC) |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | 43,004 | 3,414 | 118 | 23 | `NOASSERTION` | 2026-08-19 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 33,885 | 3,307 | 158 | 6 | MIT | 2026-08-18 |
| [Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | 8,863 | 414 | 16 | 0 | `NOASSERTION` | 2026-08-18 |

Metadata-visible scope differs:

- `academic-research-skills` uses topics for academic pipelines, academic writing,
  literature review, peer review, Claude, and prompt engineering.
- `scientific-agent-skills` uses a broad `agent-skills` topic plus many scientific
  discipline topics. Its repository description claims 163 skills; RhetoriLex did not
  treat that self-description as independent validation. The separate recursive-tree
  method below also found 163 `SKILL.md` files at the pinned commit.
- `academic-research-skills-codex` uses Codex, academic research/writing, literature
  review, peer review, prompt engineering, and research-assistant topics.

These observations describe public positioning, not feature parity or quality.

## Context repositories

Four additional repositories were selected from relevant topic/keyword result sets to
show adjacent product forms. RhetoriLex itself is included as baseline.

| Repository | Original category annotation | Stars | Forks | Watchers | API license | Last push (UTC) |
| --- | --- | ---: | ---: | ---: | --- | --- |
| [ahmetbersoz/chatgpt-prompts-for-academic-writing](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing) | academic-writing prompt collection | 4,897 | 391 | 43 | `null` | 2024-01-25 |
| [OpenNSWM-Lab/FAROS](https://github.com/OpenNSWM-Lab/FAROS) | research workflow/orchestration system | 2,997 | 349 | 268 | `null` | 2026-08-12 |
| [delibae/claude-prism](https://github.com/delibae/claude-prism) | offline scientific-writing workspace | 1,747 | 157 | 13 | MIT | 2026-07-28 |
| [Epsilon617/Codex-Academic-Skills](https://github.com/Epsilon617/Codex-Academic-Skills) | Codex academic skill collection | 170 | 7 | 1 | MIT | 2026-06-16 |
| [rezaprama/RhetoriLex](https://github.com/rezaprama/RhetoriLex) | evidence-calibrated rhetorical-move catalog | 1 | 0 | 0 | Apache-2.0 | 2026-08-19 |

The category column is a compact RhetoriLex classification based on repository names,
topics, and product form; it is not copied description text.

## Commit-pinned `SKILL.md` footprint

| Repository | Commit | `SKILL.md` files | Tree truncated |
| --- | --- | ---: | --- |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | `5714f3a3eb83` | 4 | no |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | `48dc1cf173f0` | 163 | no |
| [Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | `d5e66fb0d9e4` | 2 | no |
| [Chen-ShiRui/claude-academic-skills](https://github.com/Chen-ShiRui/claude-academic-skills) | `7ed6377f0efb` | 24 | no |
| [FabianRitter/paper-writing-agents](https://github.com/FabianRitter/paper-writing-agents) | `96921148976a` | 3 | no |
| [HZ-KMNO/top-journal-manuscript-skill](https://github.com/HZ-KMNO/top-journal-manuscript-skill) | `426b50f668d3` | 1 | no |

Repository organization varies. One `SKILL.md` can expose multiple operations; many
files can be variants or narrow modules. Counts cannot be compared as capability scores.
Exact SHAs and method are in
[`data/discovery/github-skill-files-2026-08-19.json`](../data/discovery/github-skill-files-2026-08-19.json).

## Topic landscape

| GitHub topic | Matching repositories |
| --- | ---: |
| `agent-skills` | 16,343 |
| `research-tools` | 1,121 |
| `academic-writing` | 1,004 |
| `literature-review` | 879 |
| `scientific-writing` | 243 |
| `rhetoric` | 36 |
| `research-writing` | 31 |

Topic counts show available repositories carrying maintainer-selected labels. They do
not measure audience demand. GitHub search limits returned result lists even when it
reports a larger `total_count`, and counts can move with indexing and topic edits.

## Positioning implications

The landscape contains high-visibility broad skill collections, research workflows,
prompt collections, and writing workspaces. RhetoriLex should not imply that it replaces
those categories or compete on raw file count. Its verifiable role is narrower:

- a structured lexicon of rhetorical moves rather than a full research pipeline;
- an explicit evidence/claim-strength contract rather than generic wording retrieval;
- causal-design safeguards and protected semantic slots;
- one deterministic offline catalog exposed through API, CLI, browser, and Agent Skill;
- original editorial data with documented clean-room provenance.

This makes RhetoriLex useful as a focused component inside human and agent workflows.
Interoperability and auditability are stronger, supportable claims than breadth or
popularity.

No conclusion is drawn that adjacent repositories lack these properties; their content
was not copied or evaluated feature-by-feature in this study.

## Repository About recommendation

**Description**

> Open academic and scientific writing phrasebank, rhetorical moves, and evidence-safe research writing skills for papers, theses, literature reviews, and manuscripts.

**Homepage**

<https://rezaprama.github.io/RhetoriLex/>

**Topics**

- `academic-writing`
- `scientific-writing`
- `research-writing`
- `academic-english`
- `phrasebank`
- `rhetorical-moves`
- `literature-review`
- `research-tools`
- `agent-skills`
- `codex`
- `evidence-based`
- `python`

This set follows measured topic/keyword relevance plus verified product compatibility.
It does not turn repository counts into a demand claim and should be reviewed after a
measured discovery cycle, not changed in response to single-day star movements.

## Boundaries and gates

- Metrics are snapshots, never timeless “current” values.
- Stars indicate bookmarking/appreciation behavior; they are not users or quality scores.
- Watchers use `subscribers_count`, not legacy `watchers_count`.
- Open-issue counts are not defect rates.
- Push recency is activity metadata, not maintenance quality.
- API license fields are discovery metadata, not rights clearance.
- `SKILL.md` counts are file footprints, not feature or quality rankings.
- No repository content, prompt, skill instruction, template, or README prose is reused.
- Any future feature comparison needs a separate protocol and source-by-source rights
  review.

## Structured evidence

- [`github-landscape-2026-08-19.json`](../data/discovery/github-landscape-2026-08-19.json)
- [`github-skill-files-2026-08-19.json`](../data/discovery/github-skill-files-2026-08-19.json)
- [`discovery-signals-2026-08-19.json`](../data/discovery/discovery-signals-2026-08-19.json)
- [`discovery-research.md`](discovery-research.md)

Research captured on 2026-08-19. Repository metrics can change after every refresh.
