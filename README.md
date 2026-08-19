# RhetoriLex

**Evidence-calibrated rhetorical moves for academic writing. Offline, inspectable, and clean-room by design.**

[![CI](https://github.com/rezaprama/RhetoriLex/actions/workflows/ci.yml/badge.svg)](https://github.com/rezaprama/RhetoriLex/actions/workflows/ci.yml)
[![Pages](https://github.com/rezaprama/RhetoriLex/actions/workflows/pages.yml/badge.svg)](https://github.com/rezaprama/RhetoriLex/actions/workflows/pages.yml)
[![License: Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-0f766e.svg)](LICENSE)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-0f766e.svg)](LICENSES/CC-BY-4.0.txt)

[Explore the catalog](https://rezaprama.github.io/RhetoriLex/) · [Bahasa Indonesia](README.id.md) · [Agent Skill](skills/rhetorilex/SKILL.md) · [Provenance](PROVENANCE.md)

RhetoriLex helps a writer choose language from communicative purpose and evidence, not from how academic it sounds. Its initial release contains 48 independently authored templates across 12 rhetorical functions, with explicit claim strength, evidence requirements, causal-design guards, risk, slots, and provenance.

It does not write evidence for you. It does not invent citations. It does not turn an association into a cause.

## Why it is different

- **Evidence before polish.** Every pattern declares the minimum evidence and strongest compatible claim.
- **Meaning-preserving.** The Agent Skill protects citations, numbers, units, populations, negation, uncertainty, and causal status during rewriting.
- **Clean-room catalog.** Released wording is original editorial work with `source_reuse: false`. Restricted source inventories are excluded.
- **Offline core.** Search, filters, validation, builds, and the Skill helper use Python's standard library only.
- **One source of truth.** Canonical JSONL deterministically produces JSON, CSV, SQLite, Markdown, package resources, Skill assets, and checksums.
- **Three useful surfaces.** Use the Python API/CLI, portable Agent Skill/plugin, or static browser explorer.

## Try it

```bash
git clone https://github.com/rezaprama/RhetoriLex.git
cd RhetoriLex
python -m pip install -e .
rhetorilex search "cautious interpretation" --stage discussion --limit 3
```

Machine-readable output and hard evidence filters:

```bash
rhetorilex --json search "observational result" \
  --evidence observational \
  --max-claim-strength bounded \
  --risk low
```

Inspect one pattern or the full contract health:

```bash
rhetorilex explain RLX-QUA-001
rhetorilex inspect --validate
rhetorilex taxonomy rhetorical_functions
```

Python API:

```python
from rhetorilex import Catalog

catalog = Catalog.load()
results = catalog.search(
    "state a limitation",
    stage="discussion",
    max_claim_strength="bounded",
    limit=3,
)

for result in results:
    print(result.entry.template, result.entry.evidence_requirement)
```

## Install the Agent Skill

For one repository, copy `skills/rhetorilex` to `.agents/skills/rhetorilex`. For personal use across projects, copy it to `~/.codex/skills/rhetorilex`.

The Skill can route requests such as:

- “Give three cautious ways to interpret this observational result.”
- “Rewrite this paragraph without changing citations, values, or claim strength.”
- “Compare options for stating a bounded research gap.”
- “Audit this sentence for causal overclaiming.”

It intentionally refuses citation fabrication, plagiarism disguise, synonym spinning, detector evasion, and unsupported claim upgrades. A release-ready plugin archive is also published from the repository manifest at [.codex-plugin/plugin.json](.codex-plugin/plugin.json).

## Catalog model

Each canonical entry includes:

| Field | Purpose |
| --- | --- |
| `function` | Stable communicative purpose such as `identify_gap` or `state_limitation` |
| `template` | Original wording with explicit named slots |
| `stage` | Compatible manuscript stage |
| `claim_strength` | `tentative`, `bounded`, `assertive`, or `causal` |
| `evidence_requirement` | `none`, `contextual`, `observational`, `direct`, or `convergent` |
| `causal_design_required` | Prevents causal patterns from being treated as generic prose |
| `risk` | Editorial review level: `low`, `medium`, or `high` |
| `provenance` | Required `original_editorial` and `source_reuse: false` record |

See [data/taxonomy/taxonomy.v1.json](data/taxonomy/taxonomy.v1.json), [data/contracts/evidence-claim.v1.json](data/contracts/evidence-claim.v1.json), and [docs/data-model.md](docs/data-model.md).

## Build and verify

```bash
python scripts/validate_data.py
python scripts/build_data.py
python -m unittest discover -s tests -v
python scripts/package_plugin.py --output dist/rhetorilex-plugin.zip
```

The test suite checks schemas, provenance, slot equality, evidence requirements, causal guards, deterministic builds, retrieval behavior, frozen benchmark routing, CLI behavior, and contract safety. Continuous integration repeats builds and compares checksums.

## Architecture

```text
data/canonical/catalog.v1.jsonl
          |
          +--> data/dist/*                    portable data artifacts
          +--> src/rhetorilex/resources/*     Python package
          +--> skills/rhetorilex/assets/*     offline Agent Skill
          +--> docs/data/phrases.json          assembled Pages artifact

taxonomy + JSON Schema + evidence contract
          |
          +--> validator --> tests --> deterministic release gate
```

The browser explorer is static HTML, CSS, and JavaScript. It has no account, backend, CDN dependency, or telemetry.

## Source and rights boundary

The private workbook supplied for this project carries an academic-use and no-redistribution notice. It was inspected locally only for non-expressive aggregate structure and quality signals. It is ignored by Git, its cells and labels are absent from this repository, every migration candidate remains unresolved, and **zero source-derived items were promoted**.

Manchester Academic Phrasebank is citation/conceptual context only; its phrase inventory was not imported or rewritten. BAWE is excluded. The Elsevier OA CC-BY Corpus v3 is registered only as a possible future aggregate-validation source and was not ingested. Full decisions, source links, and review rules are in [PROVENANCE.md](PROVENANCE.md), [data/sources/source-registry.yaml](data/sources/source-registry.yaml), and [reports/xlsx-audit.md](reports/xlsx-audit.md).

## Contributing

Contributions are welcome when wording is independently authored and evidence-safe. Start with [CONTRIBUTING.md](CONTRIBUTING.md). New patterns require provenance, named slots, taxonomy compatibility, evidence metadata, originality review, and tests. Never attach a restricted workbook, source inventory, manuscript, or corpus excerpt to an issue or pull request.

Security, confidential-draft, provenance, and rights concerns belong in the private process described by [SECURITY.md](SECURITY.md). Project decisions are recorded in [GOVERNANCE.md](GOVERNANCE.md) and [IMPLEMENTATION_LOG.md](IMPLEMENTATION_LOG.md).

## License and citation

Software, configuration, tests, and Agent Skill code are Apache-2.0. Original data, reports, benchmarks, assets, and documentation are CC BY 4.0. Machine-readable path mapping lives in [REUSE.toml](REUSE.toml); third-party status lives in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Citation metadata is available in [CITATION.cff](CITATION.cff). Licensing documents state project policy, not legal advice.
