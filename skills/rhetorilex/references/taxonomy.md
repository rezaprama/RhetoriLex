# Rhetorical Routing

RhetoriLex uses a clean-room functional model:

```text
communicative goal
  -> evidence role
  -> rhetorical relation
  -> stance
  -> reader guidance
  -> genre and discipline constraints
```

Use this model internally. Users should not need taxonomy identifiers.

## Evidence roles

- establish a problem, boundary, gap, aim, or contribution;
- attribute, compare, synthesise, qualify, or challenge scholarship;
- describe design, sampling, materials, procedure, analysis, validation, or ethics;
- report quantities, patterns, associations, uncertainty, null findings, or robustness;
- interpret findings, compare explanations, bound generalisation, or state implications;
- respond to reviewers, explain revisions, disclose availability, or state competing interests.

## Relations

- continuation, sequence, exemplification, specification;
- comparison, contrast, concession, correction;
- evidence, interpretation, condition, limitation;
- association, prediction, influence, cause;
- backward reference, forward reference, and section transition.

## Routing a passage

For a single sentence, identify one primary move and optional secondary relation. For a paragraph, plan an ordered move chain. A discussion paragraph, for example, might report the finding, compare prior work, offer a bounded interpretation, consider an alternative, and state a limitation. Do not assume that every paragraph needs every move.

Section conventions are priors, not rules. A phrase acceptable in Discussion may be interpretive overreach in Results. Discipline metadata is a scope constraint, not decoration.

Use stable semantic IDs from the bundled taxonomy only when producing machine-readable output. Retrieve current IDs with `python scripts/search.py --taxonomy` rather than guessing.
