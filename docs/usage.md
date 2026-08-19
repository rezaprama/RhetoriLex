# Usage guide

## Choose a mode

Use **search** when you know the writing intent. Use **suggest** when you know only the beginning of a function, title, or keyword. Use **explain** before adapting a high-risk pattern. Use **inspect** for catalog health. Use **taxonomy** for stable IDs. Use **random** only for discovery, never as evidence that a pattern fits.

## Search examples

```bash
rhetorilex search "bounded research gap" --stage introduction
rhetorilex search "interpret estimate" --evidence observational --max-claim-strength bounded
rhetorilex search "causal effect" --function causal_claim --risk high
rhetorilex --json search "state limitation" --discipline health_sciences
```

Filters are hard constraints. Ranking is a retrieval signal, not a scientific-validity score.

## Safe adaptation

1. Identify the intended rhetorical move.
2. Record protected facts: citations, values, units, direction, population, intervention/exposure, comparator, outcome, uncertainty, negation, limitations, and causal status.
3. Set the maximum supported claim strength.
4. Retrieve one to three candidates with compatible filters.
5. Fill named slots using only supplied evidence.
6. Compare the result with the protected facts.
7. Reject wording that changes scope or implication.

Example with observational evidence:

```text
Evidence: In the adjusted cohort model, X was associated with Y (RR 1.21, 95% CI 1.04 to 1.41).
Safe move: "The adjusted estimate is consistent with an association between X and Y in this cohort."
Unsafe move: "X increased Y."
```

The safe sentence still needs the relevant citation and may need covariates, population, time, or residual-confounding context.

## API notes

`Catalog.load()` reads package resources and makes no network call. Catalog entries are immutable dataclasses. Search ties are resolved by stable ID, which keeps repeated builds and tests predictable.

`max_claim_strength` uses this order:

```text
tentative < bounded < assertive < causal
```

The order is a catalog control. It is not a universal ranking of every English verb or sentence.

## Agent Skill notes

The Skill retrieves only when wording options or comparisons help. It should plan the move before phrasing, load only relevant references, return a small candidate set, and explain evidence conditions. It should refuse requests to fabricate, disguise copying, or evade detection while offering an integrity-preserving alternative.
