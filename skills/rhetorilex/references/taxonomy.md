# Rhetorical Routing

RhetoriLex uses a clean-room functional model:

```text
writing goal
  -> paper section or publication task
  -> rhetorical move
  -> evidence role and claim ceiling
  -> domain and discipline
  -> reader guidance
```

Use this model internally. Users should not need taxonomy IDs.

## Skill areas

The generated catalog assigns multiple derived skill areas to each pattern:

- `research_framing`: context, scope, gap, position, contribution;
- `literature_writing`: attribution, comparison, contrast, synthesis;
- `argumentation`: position, qualification, interpretation, contribution;
- `thesis_dissertation`: framing, methods, boundaries, limitations, contribution;
- `publication`: contribution, implications, reviewer response;
- `scientific_framing`: evidence, null results, uncertainty, causal claims;
- `methods`, `results`, and `discussion`: section-centered browsing;
- `claim_control`: qualification, null evidence, causal boundaries;
- `evidential_verbs`: attribution and empirical force;
- `reviewer_response` and `paraphrasing`: publication-integrity tasks.

One pattern may serve several areas. Filter by a skill area to narrow discovery, then check the pattern's exact function.

## Domains and disciplines

Domains are derived from explicit discipline metadata rather than guessed from wording: general academic, humanities/interpretive, social/behavioral, quantitative empirical, qualitative inquiry, experimental science, clinical/health, engineering/computing, legal/policy, and business/management.

Domain fit is a scope constraint, not decoration. A general pattern is cross-disciplinary; it does not override specialized reporting conventions.

## Paper-section routing

- **Abstract:** problem, aim, method, principal result, bounded conclusion.
- **Introduction:** context, gap, scope, question, position, contribution.
- **Literature review:** attribution, comparison, disagreement, synthesis, source-dependent paraphrase.
- **Methods:** design, population, material, procedure, model, rationale, boundary.
- **Results:** estimates, patterns, associations, uncertainty, null findings, contrasts.
- **Discussion:** interpretation, alternatives, causal limits, generalisation, implications.
- **Limitations and conclusion:** inferential boundaries, contribution, proportionate next steps.
- **Peer-review response:** concern, decision, evidence, revision, manuscript location.

Section conventions are priors. Results language should not acquire unsupported interpretation merely because a pattern is fluent.

## Move chains

For one sentence, identify a primary move and optional relation. For a paragraph, plan an ordered chain. A discussion paragraph may report the finding, compare prior work, offer a bounded interpretation, consider an alternative, and state a limitation. Do not force every move into every paragraph.

Use stable semantic IDs only for machine-readable output. Discover current values with:

```bash
python scripts/search.py --list-functions
python scripts/search.py --list-sections
python scripts/search.py --list-domains
python scripts/search.py --list-skill-areas
```