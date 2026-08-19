# Evidence Preservation Contract

Apply to every rewrite, paraphrase, compression, or style change.

## Protected elements

- citations and attribution boundaries;
- quotation boundaries and quoted wording;
- integers, decimals, signs, percentages, ranges, dates, units, sample sizes, and statistical values;
- named variables, instruments, populations, settings, interventions, comparators, and outcomes;
- effect direction, ordering, and reference group;
- negation and exception language;
- modality, uncertainty, limitations, and scope;
- study design, evidential source, claim strength, and causal status.

## Procedure

1. **Inventory:** extract protected elements before drafting. Resolve pronouns only when their referents are unambiguous.
2. **Model:** write a compact proposition map: actor or population, relation, object or outcome, direction, scope, evidence, uncertainty, attribution.
3. **Transform:** change syntax, information order, or register while keeping the proposition map fixed.
4. **Compare:** align every protected element in source and draft. A missing, added, or altered element is a failure unless the user explicitly requested that change.
5. **Calibrate:** compare claim-strength and causal levels separately from surface similarity.
6. **Report:** if a safe rewrite is impossible because source meaning is unclear, preserve the ambiguity and flag it.

## Failure conditions

Reject or repair a draft that:

- drops a citation or changes which proposition it supports;
- changes `not`, `only`, `except`, direction, comparator, population, or time period;
- rounds or reformats a value in a way that changes meaning;
- replaces uncertainty with certainty;
- adds importance, mechanism, novelty, generality, or causality;
- converts an author-attributed claim into an unqualified fact;
- blends quoted and paraphrased wording.

Formatting may change only when value and precision remain equivalent. Keep original significant figures unless the user asks to recalculate or restyle them.

## Compact audit format

Use when the user asks for a check:

```text
Verdict: pass | revise | fail
Preserved: citations; values; direction; scope; uncertainty; causal status
Changed: <specific element or none>
Repair: <minimal safe revision, when needed>
```
