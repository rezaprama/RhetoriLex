# Offline Retrieval

The bundled search script reads independently authored pattern metadata from `assets/patterns.json`. It requires Python 3.10+ and no third-party package.

Run commands from the skill directory:

```bash
python scripts/search.py "research gap" --limit 3
python scripts/search.py "null finding" --section discussion --max-claim-strength tentative
python scripts/search.py "compare findings" --function compare_findings --json
```

Available filters are `--section` (alias `--stage`), `--function`, `--evidence`, `--max-claim-strength`, `--discipline`, `--risk`, and `--limit`. Add `--json` for machine-readable output.

## Ranking

Ranking combines:

1. token coverage across ID, title, template, description, function, stage, and keywords;
2. an exact substring bonus for the complete query;
3. bounded fuzzy similarity across the same fields;
4. stable ID ordering to break equal scores reproducibly.

Section, function, evidence, claim-strength, discipline, and risk filters are hard constraints rather than ranking factors. Search score does not make a candidate scientifically appropriate. Check evidence compatibility after retrieval.

## Context discipline

- Retrieve three candidates by default.
- Load only returned records, not the complete asset.
- Prefer structurally distinct candidates instead of superficial variants.
- Explain slots such as `{finding}`, `{population}`, or `{citation}`.
- Do not fill a slot with invented content.
- If no candidate fits, describe the needed move in plain language rather than forcing a poor result.

If `assets/patterns.json` is absent, report that the distribution asset was not built. In a full repository checkout, run `python scripts/build_data.py` from repository root, then retry.
