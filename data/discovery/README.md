# Discovery datasets

This directory stores reproducible discovery and repository-landscape observations.
It contains public metadata and RhetoriLex annotations only. No third-party repository
content, prompts, skills, templates, or README prose is copied here.

## Files

- `github-landscape-2026-08-19.json`: one timestamped GitHub REST API snapshot for the
  three requested comparison repositories, four context repositories, and RhetoriLex.
- `github-skill-files-2026-08-19.json`: commit-pinned recursive-tree counts of `SKILL.md`
  files for six relevant repositories; file count is not capability or quality.
- `discovery-signals-2026-08-19.json`: topic counts, keyword-query counts, and explicit
  unavailable measurements.
- `keyword-research.json`: stable, deterministic keyword export using the required
  `keyword`, `source`, `geography`, `language`, `time_window`, `metric`, `value`,
  `retrieved_at`, `confidence`, and `notes` contract.

## Observation contract

Every discovery signal records:

- `source`: measurement provider;
- `geo`: geographic scope, or `not_applicable` when the source has none;
- `language`: query language, not a claim about repository language;
- `window`: time or index scope;
- `metric` and `value`: measured quantity and result;
- `retrieved_at`: UTC capture time;
- `confidence`: `high`, `medium`, or `unavailable`;
- `notes`: interpretation and limitations.

Additional fields such as `query`, `unit`, and `source_url` make each observation
reproducible. A `null` value means no direct measurement was obtained; it must never be
converted into zero.

## Interpretation rules

GitHub search counts measure repository supply in GitHub's current index. They are not
web-search volume, user demand, adoption, quality, or market size. Topic counts depend
on maintainer-assigned labels. Keyword counts depend on GitHub indexing and query
semantics. Counts can change immediately after capture.

GitHub documents that `subscribers_count` is the watcher count, while legacy
`watchers`, `watchers_count`, and `stargazers_count` are star counts. This dataset
therefore labels only `subscribers_count` as watchers.

Direct Google Trends measurement was attempted but no reproducible export was
retrieved in this environment. Both Worldwide and Indonesia records are preserved as
`value: null` with `confidence: unavailable`; no proxy or invented search volume is
substituted.

## Reproduction

Repository metadata:

```bash
gh api repos/OWNER/REPOSITORY
```

Repository search count:

```bash
gh api -X GET search/repositories \
  -f q='topic:academic-writing' \
  -f per_page=1
```

Check `total_count`, `incomplete_results`, and capture time together. See the official
[repository search endpoint](https://docs.github.com/en/rest/search/search#search-repositories),
[repository endpoint](https://docs.github.com/en/rest/repos/repos#get-a-repository), and
[watching semantics](https://docs.github.com/en/rest/activity/watching#about-watching).

## Rights

The original selection, schema, notes, and annotations are licensed under CC BY 4.0
through the repository's `REUSE.toml`. Repository names, topics, counts, and other
third-party facts remain subject to applicable rights and platform terms. This is
research metadata, not legal advice.
