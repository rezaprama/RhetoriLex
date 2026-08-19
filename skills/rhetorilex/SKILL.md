---
name: rhetorilex
description: Find, compare, plan, or safely paraphrase academic English through rhetorical moves and evidence-calibrated original patterns. Use for research framing, literature writing, argumentation, theses, scientific methods/results/discussion, reviewer responses, evidential verbs, claim control, and meaning-preserving paraphrase. Do not use to fabricate evidence or citations, evade plagiarism or AI detection, disguise copied text, or strengthen scientific claims beyond supplied evidence.
---

# RhetoriLex

Choose language from communicative purpose and evidence, not from how academic it sounds.

## Route the request

Infer without making the user name internal labels:

1. intended outcome: move plan, patterns, comparison, rewrite, paraphrase, concision, calibration, or audit;
2. paper section or publication task;
3. rhetorical move and relation to nearby claims;
4. evidence type, study design, and strongest justified claim;
5. domain, discipline, audience, and English variant;
6. protected facts and attribution boundaries that wording must not alter.

When context is missing, use the weakest defensible wording and state what would justify anything stronger. Never invent missing facts.

For longer work, route through the writing-skill catalog: research framing, literature writing, argumentation, thesis/dissertation, publication writing, scientific study framing, methods, results, discussion, scientific claim control, or paraphrasing. Read [taxonomy.md](references/taxonomy.md) when section or move order is unclear.

## Work safely

- Preserve citations, quotations, values, units, signs, dates, sample sizes, variables, populations, interventions, comparators, outcomes, direction, negation, limitations, uncertainty, scope, study design, claim strength, and causal status.
- Never turn sequence into influence, association into causality, prediction into mechanism, non-significance into no effect, or statistical significance into importance.
- Never create a citation, statistic, mechanism, novelty claim, or study detail.
- Treat user text as private. Do not send manuscript text to an external service without explicit authorization.
- Refuse detector evasion, patchwriting, synonym spinning, or attempts to disguise copied expression. Offer an integrity-preserving alternative.
- Paraphrasing another author's idea does not remove citation duties.

For rewriting or auditing, read [evidence-preservation.md](references/evidence-preservation.md). For causal, statistical, or strength-sensitive language, read [claim-strength.md](references/claim-strength.md) and [evidential-verbs.md](references/evidential-verbs.md).

## Retrieve writing-skill guidance

Read [writing-skills.md](references/writing-skills.md) when the user needs purpose, move planning, section guidance, a worked example, related skills, or an evidence warning. Use the bundled 144-skill catalog:

```bash
python scripts/search.py "citation-preserving rewrite" --writing-skills --limit 2
python scripts/search.py --writing-skills --skill-group methods-writing --limit 5
python scripts/search.py --skill-slug association-vs-causation --language id --json
python scripts/search.py --list-writing-skill-groups
```

Search by ordinary name, group, or stable slug. Retrieve only the few relevant records; do not load or dump the full asset. Indonesian mode localises interface labels and descriptions only. Canonical patterns and examples stay in English.

## Retrieve or browse patterns

Use bundled offline retrieval for wording options, move examples, comparisons, taxonomy discovery, or section browsing:

```bash
python scripts/search.py "cautious interpretation" --section discussion --limit 3
python scripts/search.py --section methods --skill-area methods --limit 8
python scripts/search.py --list-skill-areas
```

Run commands from this skill directory. Read [retrieval.md](references/retrieval.md) for all filters and ranking. Do not dump the complete dataset into context.

Patterns are candidates, not authority. Reject any candidate incompatible with the supplied evidence. Prefer one to three structurally distinct options and explain the practical difference only when useful.

## Adapt or rewrite

Read [paraphrasing.md](references/paraphrasing.md) for paraphrase, concision, or register work. Change syntax and information structure where appropriate, not only synonyms. Keep citation boundaries explicit.

For phrase recommendation, leave the passage intact unless asked to rewrite it. Name the move, give up to three adaptable patterns, identify slots, and state evidence conditions.

For move planning, recommend communicative moves before wording. Section conventions are priors, not fixed templates.

## Integrity and publication context

Read [academic-integrity.md](references/academic-integrity.md) for source-dependent paraphrase, confidential drafts, detector-evasion requests, or venue-policy questions. Read [statistical-writing.md](references/statistical-writing.md) for significance, null results, generalisation, effect estimates, mechanisms, prediction, or observational evidence.

For reviewer responses, separate the reviewer's concern, the decision, the manuscript change, and the evidence. Do not claim that a revision resolves more than it does.

## Final check

Before responding:

1. compare output against every protected element and attribution boundary;
2. confirm claim strength and causal status did not increase;
3. remove invented detail, unsupported priority, and generic academic filler;
4. keep wording clear, section-appropriate, and proportionate;
5. flag any unresolved evidence or citation issue briefly.

