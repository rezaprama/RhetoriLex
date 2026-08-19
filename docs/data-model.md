# Data model

This page documents canonical entry version 1. The normative validation rules are the JSON Schemas and evidence contract in `data/schema/` and `data/contracts/`.

## Canonical entry

| Field | Type | Invariant |
| --- | --- | --- |
| `id` | string | Unique, stable, uppercase `RLX-*` identifier |
| `function` | taxonomy ID | Must exist in `rhetorical_functions` |
| `title` | string | Short editorial name, not a template duplicate |
| `template` | string | Original text with Python-style named slots |
| `description` | string | Explains the move without implying new evidence |
| `stage` | taxonomy ID | Manuscript stage or `general` |
| `disciplines` | string array | One or more known discipline IDs |
| `claim_strength` | taxonomy ID | `tentative`, `bounded`, `assertive`, or `causal` |
| `evidence_requirement` | taxonomy ID | Minimum evidence declared by the pattern |
| `causal_design_required` | boolean | Must be true for a causal claim |
| `placeholders` | string array | Exact set of fields used in `template` |
| `keywords` | string array | Retrieval cues, not scientific assertions |
| `notes` | string | Conditions, limits, and slot guidance |
| `risk` | taxonomy ID | `low`, `medium`, or `high` |
| `provenance` | object | Must declare original editorial method and no source reuse |
| `version` | integer | Entry schema generation |

## Evidence and claim contract

Claim strength is an upper bound, not a promise that a filled sentence is valid.

| Claim strength | Minimum evidence | Causal design |
| --- | --- | --- |
| `tentative` | `none` | Not required |
| `bounded` | `contextual` | Not required |
| `assertive` | `observational` | Not required |
| `causal` | `direct` | Required |

An editor must still inspect design quality, identification assumptions, measurement, uncertainty, scope, and how slots are filled. A source classified as direct does not automatically license causal language.

## Provenance object

Release entries require:

```json
{
  "method": "original_editorial",
  "author": "RhetoriLex contributors",
  "source_reuse": false
}
```

This is a release gate, not a declaration that a short phrase can never resemble ordinary language elsewhere. Contributions must still pass overlap and editorial review under `PROVENANCE.md`.

## Generated formats

`scripts/build_data.py` exports:

- wrapped JSON for APIs and packages;
- flat CSV for spreadsheets and lightweight analysis;
- SQLite for local structured queries;
- Markdown for review;
- SHA-256 checksum manifests;
- package and Skill resource copies.

Only canonical JSONL, taxonomy, contract, and schemas should be edited directly.
