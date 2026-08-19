# Architecture

RhetoriLex is an offline-first reference implementation. The core has zero runtime dependencies and keeps editorial data, semantic contracts, rendering, and agent behavior separable.

## Data flow

```text
canonical JSONL
  + taxonomy
  + JSON Schema
  + evidence-claim contract
          |
          v
  validate_data.py
          |
          v
   build_data.py
     |       |        |         |
     v       v        v         v
   JSON     CSV     SQLite   Markdown
     |                          |
     +--> Python resources      +--> human review
     +--> Agent Skill asset
     +--> GitHub Pages artifact
```

Canonical entries are sorted and serialised predictably. Generated artifacts must not be edited by hand. Continuous integration builds twice in separate directories and compares checksums.

## Components

### Canonical data

`data/canonical/catalog.v1.jsonl` is the editorial source of truth. One JSON object occupies one line. Stable IDs permit deprecation and migration without silently changing an existing meaning.

### Semantic controls

- `data/taxonomy/taxonomy.v1.json` defines stable rhetorical functions, stages, disciplines, claim strengths, evidence requirements, and risk levels.
- `data/contracts/evidence-claim.v1.json` defines the evidence floor for each claim strength and the causal-design guard.
- `data/schema/*.schema.json` makes structural rules portable to tools outside Python.

### Python package

`src/rhetorilex` loads immutable bundled resources with `importlib.resources`. `Catalog` provides deterministic get, filter, exact/lexical/fuzzy search, suggestions, seeded random selection, and health counts. The CLI is a thin interface over the same API.

### Agent Skill and plugin

`skills/rhetorilex` is portable. `SKILL.md` contains routing and safety instructions; references are loaded only for relevant tasks; `scripts/search.py` searches the bundled asset without requiring the package; `agents/openai.yaml` provides UI metadata. `.codex-plugin/plugin.json` exposes the skill as a distributable plugin.

### Explorer

`docs/` contains semantic HTML, CSS, and JavaScript. Deployment copies the generated `phrases.json` into the assembled Pages artifact. The explorer performs local filtering and ranking. It has no backend, analytics, account, external font, or CDN dependency.

## Trust boundaries

| Boundary | Rule |
| --- | --- |
| User manuscript | Process only for the requested response; never add it to catalog or telemetry |
| Restricted source | Keep outside Git, logs, fixtures, screenshots, generated artifacts, and prompts |
| External corpus | Deny ingestion until license, checksum, attribution, minimisation, and leakage review pass |
| Canonical contribution | Require original wording, provenance fields, evidence metadata, schema checks, and review |
| Generated artifact | Rebuild from canonical data; verify checksum and do not hand-edit |

## Failure behavior

- Unknown taxonomy IDs fail validation.
- Duplicate IDs fail catalog loading and validation.
- Placeholder declarations must exactly match template fields.
- Evidence-bearing patterns require an evidence-like slot.
- Causal patterns require direct evidence, a credible causal design, and high risk.
- Missing resources fail loudly instead of falling back to network access.

## Versioning

Package, taxonomy, contracts, and data artifacts follow semantic versioning. A new stable ID or additive field can be a minor version. Changed meaning, incompatible taxonomy semantics, or contract weakening requires a major version. Deprecation should preserve the old ID and provide a replacement path.
