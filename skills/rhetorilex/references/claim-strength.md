# Claim Strength Contract

Use this contract whenever wording could change what evidence supports. It is a reasoning aid, not a universal dictionary ranking. Context, syntax, discipline, study design, and accompanying qualification can change force.

## Working ladder

0. **Observation:** reports a measured value, event, or textual feature without a broader relation.
1. **Pattern:** describes recurrence, distribution, contrast, or trend.
2. **Association:** states that variables co-vary without assigning cause.
3. **Prediction:** states that information improves prediction, which does not by itself establish cause.
4. **Interpretation:** offers an evidence-linked explanation or meaning, explicitly open to alternatives.
5. **Influence or effect:** attributes change to an exposure or intervention but may remain short of a fully identified causal effect.
6. **Causation:** states that changing X changes Y under the relevant counterfactual conditions.

## Runtime labels

The bundled catalog compresses the reasoning ladder into four retrieval labels:

- `tentative`: observation, pattern, or explicitly cautious interpretation;
- `bounded`: scoped association, prediction, or interpretation;
- `assertive`: direct, well-supported noncausal finding;
- `causal`: causal claim supported by a credible design and explicit assumptions.

`--max-claim-strength` is an upper bound on candidate language, not a verdict that the user's evidence reaches that level.

Move sideways or downward without special permission. Move upward only when the user supplies evidence and design features that justify it.

## Required checks

Before choosing language, identify:

- study design and identification strategy;
- temporal order;
- comparator or counterfactual;
- confounding and selection controls;
- effect estimate and uncertainty;
- population and setting;
- whether the sentence reports authors' interpretation or the current writer's claim.

Randomisation can support causal interpretation when implementation, adherence, missingness, estimand, and analysis also support it. Observational evidence can support causal inference only with an explicit defensible design and assumptions. Never infer eligibility from a study label alone.

## Unsafe upgrades

- `was associated with` to `caused`, `led to`, or `resulted in`
- `may suggest` to `shows`, `establishes`, or `confirms`
- `occurred after` to `was produced by`
- `predicts` to `influences`
- `consistent with` to `demonstrates`
- `no statistically significant difference` to `no difference` or `equivalent`

## Response behavior

If requested wording is too strong:

1. name the mismatch briefly;
2. retain the supported level;
3. provide up to three calibrated alternatives;
4. state what evidence would be needed for the stronger form.

Do not present verbs as a context-free universal scale. Explain their force in the sentence at hand.
