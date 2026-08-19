# Offline Retrieval

The bundled script searches 96 independently authored patterns from `assets/patterns.json`. It requires Python 3.10+ and no third-party package. Generated records carry section, discipline, domain, skill-area, claim, evidence, risk, and search-alias facets.

Run commands from the skill directory:

```bash
python scripts/search.py "research gap" --limit 3
python scripts/search.py "non significant result" --section results --max-claim-strength tentative
python scripts/search.py --section methods --skill-area methods --limit 10
python scripts/search.py "ethical paraphrase" --skill-area paraphrasing --json
python scripts/search.py --list-functions
python scripts/search.py --list-sections
python scripts/search.py --list-domains
python scripts/search.py --list-skill-areas
python scripts/search.py --taxonomy
```

Available filters: `--section` (alias `--stage`), `--function`, `--evidence`, `--max-claim-strength`, `--discipline`, `--domain`, `--skill-area`, `--risk`, and `--limit`. A query is optional when at least one browse filter is present. Add `--json` for machine-readable pattern output.

## Ranking

Ranking combines:

1. token coverage across ID, title, template, description, function, section, keywords, domains, and skill areas;
2. curated aliases for common writing intents and disciplinary vocabulary;
3. a complete-query substring bonus;
4. bounded fuzzy similarity;
5. stable ID ordering for deterministic ties.

All filters are hard constraints. A high score means discoverability, not scientific appropriateness. Check evidence and attribution compatibility after retrieval.

## Context discipline

- Retrieve three candidates by default.
- Load only returned records, not the complete asset.
- Prefer structurally distinct candidates over superficial variants.
- Explain slots such as `{finding}`, `{population}`, or `{source}`.
- Never fill a slot with invented content or a fabricated citation.
- Treat `search_aliases` as discovery metadata, not wording to copy automatically.
- If no candidate fits, describe the needed move rather than forcing a poor result.

`assets/patterns.json`, `assets/taxonomy.json`, and `assets/search-aliases.json` are generated from canonical data. In a full repository checkout, rebuild them with `python scripts/build_data.py` from repository root.