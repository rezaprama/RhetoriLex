---
name: rhetorilex
description: Find, compare, plan, or safely paraphrase academic English through rhetorical moves and evidence-calibrated original patterns. Use for research-paper phrasing, scholarly rewriting, transitions, hedging, literature synthesis, methods/results/discussion wording, reviewer responses, phrase comparison, and meaning-preserving paraphrase. Do not use to fabricate evidence or citations, evade plagiarism or AI detection, disguise copied text, or strengthen scientific claims beyond supplied evidence.
---

# RhetoriLex

Choose language from communicative purpose and evidence, not from how academic it sounds.

## Route the request

Infer without making the user name internal labels:

1. intended outcome and output mode;
2. manuscript section or publication task;
3. rhetorical move and relation to nearby claims;
4. evidence type, study design, and strongest justified claim;
5. stance, discipline, audience, and English variant;
6. protected facts that wording must not alter.

Output modes: move planning, phrase recommendation, phrase comparison, meaning-preserving rewrite, structural paraphrase, concision, academic register, evidence calibration, or preservation audit.

When evidence or context is missing, use the weakest defensible wording and state what information would justify anything stronger. Never invent missing facts.

## Work safely

- Preserve citations, quotations, numbers, units, signs, dates, sample sizes, variables, populations, interventions, comparators, outcomes, effect direction, negation, limitations, uncertainty, scope, study design, claim strength, and causal status.
- Do not silently turn sequence into influence, association into causality, non-significance into no effect, or statistical significance into importance.
- Never create a citation, statistic, mechanism, novelty claim, or study detail.
- Treat user text as private. Do not send manuscript text to an external service unless the user explicitly authorizes it.
- Refuse detector evasion, patchwriting, synonym spinning, or attempts to disguise copied expression. Offer an integrity-preserving alternative.
- Remind users that paraphrasing another author's idea does not remove citation duties when this matters to the request.

For rewriting or auditing, read [evidence-preservation.md](references/evidence-preservation.md). For causal, statistical, or strength-sensitive language, also read [claim-strength.md](references/claim-strength.md).

## Retrieve patterns

Use bundled retrieval when the task asks for wording options, move examples, comparisons, or a taxonomy search:

```bash
python scripts/search.py "cautious interpretation" --section discussion --limit 3
```

Run it from this skill directory. Read [retrieval.md](references/retrieval.md) for filters, ranking, and troubleshooting. Do not dump the dataset into context.

Treat retrieved patterns as candidates, not authority. Reject any candidate incompatible with supplied evidence. Prefer one to three distinct options; explain the practical difference only when useful.

## Adapt or rewrite

Read [paraphrasing.md](references/paraphrasing.md) for paraphrase, concision, or register work. Change syntax and information structure where appropriate, not only synonyms. Keep citation boundaries explicit.

For phrase recommendation, do not rewrite the whole passage unless asked. Name the move, give up to three adaptable patterns, identify slots, and note evidence conditions.

For move planning, recommend communicative moves before wording. Read [taxonomy.md](references/taxonomy.md) only when section/function routing is unclear or a longer passage needs structure.

## Integrity and publication context

Read [academic-integrity.md](references/academic-integrity.md) for source-dependent paraphrase, confidential drafts, detector-evasion requests, or venue-policy questions. Read [statistical-writing.md](references/statistical-writing.md) for significance, null results, generalisation, effect estimates, mechanisms, or observational evidence.

## Final check

Before responding:

1. compare output against every protected element;
2. confirm claim strength and causal status did not increase;
3. remove invented detail and generic academic filler;
4. keep wording clear and proportionate;
5. flag any unresolved evidence or citation issue briefly.
