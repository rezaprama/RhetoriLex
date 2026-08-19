"""Focused English intent pages for search and agent-skill entry points."""

PAGES_EN = {
    "research_gap": {
        "kind": "article",
        "title": "How to Write a Research Gap Without Overclaiming | RhetoriLex",
        "description": "Define and write a specific research gap from reviewed evidence without claiming that no prior research exists.",
        "h1": "Write a research gap that the literature can support",
        "lede": "A defensible gap names a precise unresolved issue, its scope, and the evidence used to establish it.",
        "body": """
<section>
  <h2>What a research gap is</h2>
  <p>A research gap is not a dramatic statement that a topic has never been studied. It is a bounded account of what available evidence does not yet establish. The gap may concern a population, setting, mechanism, measure, method, time period, inconsistency, or unanswered comparison. It should lead directly to a question the present study can address.</p>
  <p>Build the claim from the <a href="{{link:literature_review}}">literature review</a>. Record the search scope, distinguish missing evidence from mixed evidence, and cite the studies that define the boundary. If the search was narrow, describe it as narrow.</p>
</section>
<section>
  <h2>Patterns for specific gaps</h2>
  <p class="phrase-template">Although [established finding] has been documented in [studied context], evidence regarding [specific unresolved issue] remains limited in [target context].</p>
  <p class="phrase-template">Studies differ in their estimates of [relation], leaving the role of [specific source of uncertainty] unresolved.</p>
  <p>The first pattern fits a coverage gap. The second fits inconsistent findings. Replace every bracket with facts supported by the review and preserve any uncertainty in the cited literature.</p>
</section>
<section>
  <h2>Connect the gap to the study</h2>
  <p>After stating the gap, explain why resolving it matters and how the research aim responds. Do not claim importance through generic language. Name the scientific, theoretical, methodological, clinical, or policy decision affected by the uncertainty. Then state an aim whose design, sample, and measures can actually address the stated issue.</p>
  <p>Search the <a href="{{link:phrase_explorer}}?q=research%20gap">Phrase Explorer</a> for additional patterns and inspect their evidence requirements.</p>
</section>
<aside class="article-note">
  <h2>Warning</h2>
  <p>A missing citation in your search is not proof that no study exists. Avoid first, never, and no research unless a documented, comprehensive review supports those words.</p>
</aside>
""",
    },
    "literature_review": {
        "kind": "article",
        "title": "How to Write a Literature Review That Synthesises | RhetoriLex",
        "description": "Write a literature review that organises, compares, and evaluates evidence instead of listing one study at a time.",
        "h1": "A literature review should synthesise, not inventory",
        "lede": "Organise sources around a question and make the basis of comparison visible to the reader.",
        "body": """
<section>
  <h2>Define the review's analytical frame</h2>
  <p>A literature review explains the state of knowledge relevant to a research decision. Choose an organising frame before drafting: competing theories, methodological families, populations, settings, outcomes, time, or patterns of agreement and disagreement. The frame should help the reader understand why studies can or cannot be compared.</p>
  <p>Create an evidence table with study design, sample, measure, estimate, limitation, and relevance. This prevents a polished synthesis from merging results that address different questions.</p>
</section>
<section>
  <h2>Write relations among studies</h2>
  <p class="phrase-template">Across [group of studies], estimates consistently indicate [shared pattern], although [design or population difference] limits direct comparison.</p>
  <p class="phrase-template">Whereas [study group A] reports [finding], studies using [method B] find [contrasting finding], suggesting that [bounded source of variation] warrants examination.</p>
  <p>Each pattern requires more than multiple citations. The cited studies must support the relation expressed by across, consistently, whereas, or contrasting. Use <a href="{{link:hedging}}">academic hedging</a> when evidence is mixed or indirect.</p>
</section>
<section>
  <h2>Move from synthesis to the research problem</h2>
  <p>End a thematic unit by stating what the synthesis establishes and what remains uncertain. A gap should follow from the reviewed evidence, not appear as an unsupported pivot. Link the limitation to the present aim only when the study can address it.</p>
  <p>Use the <a href="{{link:phrase_explorer}}?q=literature%20synthesis">Phrase Explorer</a> to retrieve comparison and synthesis patterns. Keep every citation attached to the proposition it supports.</p>
</section>
<aside class="article-note">
  <h2>Warning</h2>
  <p>Do not assign agreement, contradiction, quality, or consensus to a body of literature without criteria. A list of similar abstracts does not establish convergent evidence.</p>
</aside>
""",
    },
    "thesis": {
        "kind": "article",
        "title": "Thesis Writing: Argument, Chapters, and Contribution | RhetoriLex",
        "description": "Plan and revise a thesis as one evidence-linked argument across introduction, literature review, methods, results, and discussion.",
        "h1": "Write a thesis as one traceable argument",
        "lede": "Every chapter should advance the same research problem while making its own rhetorical contribution.",
        "body": """
<section>
  <h2>Build the thesis spine</h2>
  <p>Write four plain statements before polishing chapters: the problem, the research question, the design used to answer it, and the bounded contribution. These statements form the thesis spine. Each chapter should either establish a premise, document the response, report evidence, or interpret what that evidence supports.</p>
  <p>Map the spine across chapters. The <a href="{{link:research_gap}}">research gap</a> must lead to the aim. The methods must operationalise the aim. The results must answer the stated analyses. The discussion must not introduce a stronger question or broader population.</p>
</section>
<section>
  <h2>Use chapter-level signposting</h2>
  <p class="phrase-template">This chapter establishes [specific premise] by examining [evidence or analysis], providing the basis for [next chapter function].</p>
  <p class="phrase-template">Taken together, Chapters [X-Y] support [bounded contribution] within [population, setting, or methodological scope].</p>
  <p>Signposting should expose logical relations, not narrate document mechanics. Avoid repeatedly announcing that a chapter will discuss a topic when you can state the question or claim directly.</p>
</section>
<section>
  <h2>Revise across boundaries</h2>
  <p>Compare terminology, variables, population labels, and claim strength across the abstract, introduction, results, discussion, and conclusion. Track every major conclusion backward to a result and method. Track every question forward to an answer or an explicit statement that it remains unresolved.</p>
  <p>Use <a href="{{link:preserve_claim_strength}}">Preserve Claim Strength</a> when rewriting the abstract or conclusion, where compression often creates overclaiming.</p>
</section>
<aside class="article-note">
  <h2>Warning</h2>
  <p>A thesis contribution does not need to claim novelty at the level of an entire field. State exactly what the work adds, for whom, under which design, and with what remaining uncertainty.</p>
</aside>
""",
    },
    "methods": {
        "kind": "article",
        "title": "How to Write a Reproducible Methods Section | RhetoriLex",
        "description": "Write a methods section that makes design, sample, measures, procedures, exclusions, and analysis choices traceable.",
        "h1": "Methods writing makes analytical decisions visible",
        "lede": "A clear methods section lets readers understand what was done, why it was done, and how choices shape interpretation.",
        "body": """
<section>
  <h2>Report the design before procedural detail</h2>
  <p>Name the study design, setting, dates, population, sampling process, inclusion criteria, and unit of analysis. Then explain measures, interventions or exposures, outcomes, procedures, exclusions, and analytic choices. The order should follow the logic needed to interpret the estimates, not merely the chronology of project administration.</p>
  <p>Define who made subjective judgments, whether assessors were masked, and how disagreements were resolved. Passive voice is acceptable for routine procedures, but it should not hide responsibility for decisions.</p>
</section>
<section>
  <h2>Connect each choice to its purpose</h2>
  <p class="phrase-template">We used [method] to estimate [target quantity] because [design-relevant reason], with [assumption or limitation] considered in interpretation.</p>
  <p class="phrase-template">Observations were excluded according to the prespecified criterion [criterion]; [number or proportion] were removed before [analysis stage].</p>
  <p>State whether decisions were prespecified or data-informed. Report software and version when it affects reproducibility. Link supplementary detail without omitting information needed to understand the main analysis.</p>
</section>
<section>
  <h2>Audit methods against results</h2>
  <p>Every population count, model, subgroup, sensitivity analysis, and outcome reported later should have a methodological basis. Every method described should either produce a reported result or have a clear role. Use the <a href="{{link:results}}">results guide</a> to check this correspondence.</p>
</section>
<aside class="article-note">
  <h2>Warning</h2>
  <p>Do not use reproducible as a decorative claim. Provide the data, code, protocol, materials, or detail that the term implies, subject to ethical and legal limits.</p>
</aside>
""",
    },
    "results": {
        "kind": "article",
        "title": "How to Write Results With Estimates and Uncertainty | RhetoriLex",
        "description": "Write a results section that reports comparison, magnitude, direction, uncertainty, and missingness without causal overclaiming.",
        "h1": "Results writing reports what the analysis estimated",
        "lede": "Lead with the comparison and estimate, preserve uncertainty, and keep interpretation proportional to the design.",
        "body": """
<section>
  <h2>Give each result a complete reference frame</h2>
  <p>A result needs the outcome, groups or condition compared, direction, magnitude, unit, and uncertainty where appropriate. State the analysis population and time point when they are not already clear. Use tables for dense estimates, but make the text identify the findings that answer the research question.</p>
  <p>Do not replace an estimate with a significance label. A small p-value does not show practical importance, and a large p-value does not establish no effect. Report intervals and discuss what values remain compatible with the data.</p>
</section>
<section>
  <h2>Patterns for precise reporting</h2>
  <p class="phrase-template">Outcome Y was [estimate and unit] higher in [group A] than in [group B] ([interval]), with [relevant adjustment or analysis population].</p>
  <p class="phrase-template">The estimate was imprecise ([interval]), leaving both [scientifically relevant possibility A] and [possibility B] compatible with the data.</p>
  <p>The first pattern requires a real comparison and correct direction. The second helps describe uncertainty without turning an inconclusive result into proof of absence.</p>
</section>
<section>
  <h2>Keep design limits visible</h2>
  <p>Observational results should normally use associated with, differed, or was related to rather than caused, improved, or prevented. See <a href="{{link:association_vs_causation}}">Association vs Causation</a>. Verify every number, unit, table reference, subgroup label, and sign against the final analysis output.</p>
</section>
<aside class="article-note">
  <h2>Warning</h2>
  <p>Never infer a within-group change from separate significance tests, or a group difference from one significant and one non-significant result. Report the direct comparison.</p>
</aside>
""",
    },
    "discussion": {
        "kind": "article",
        "title": "How to Write a Discussion Without Overclaiming | RhetoriLex",
        "description": "Write a research discussion that answers the question, relates prior evidence, considers explanations, and states meaningful limits.",
        "h1": "A discussion interprets findings within their limits",
        "lede": "Answer the research question first, then explain relation, uncertainty, alternatives, implications, and scope.",
        "body": """
<section>
  <h2>Begin with the bounded answer</h2>
  <p>Open with the finding that most directly answers the research question. State it at the strength supported by the design and analysis. Do not repeat every result or begin with a claim of novelty. Explain how the finding changes, refines, or leaves unchanged the relevant understanding.</p>
  <p class="phrase-template">In [population and setting], the findings support [bounded interpretation], while uncertainty regarding [specific issue] remains.</p>
</section>
<section>
  <h2>Relate evidence without manufacturing agreement</h2>
  <p>Compare the result with prior studies on a stated basis: effect direction, magnitude, measure, population, design, or mechanism. Differences may reflect sampling, measurement, context, analysis, or chance. Present explanations as possibilities unless they were directly tested.</p>
  <p>Use <a href="{{link:hedging}}">academic hedging</a> to calibrate alternatives, not to make every sentence vague. Strong descriptive evidence can be stated directly. Explanatory claims need explicit limits.</p>
</section>
<section>
  <h2>Make limitations consequential</h2>
  <p>A limitation matters because it changes interpretation, precision, validity, transferability, or causal identification. State the likely consequence and any mitigation. Avoid a generic list that is disconnected from the conclusions. End by separating what the study establishes, what it suggests, and what should be tested next.</p>
  <p>Search the <a href="{{link:phrase_explorer}}?q=bounded%20discussion%20interpretation">Phrase Explorer</a> for bounded discussion patterns.</p>
</section>
<aside class="article-note">
  <h2>Warning</h2>
  <p>Do not strengthen language in the discussion because the result is interesting. Claim strength follows evidence, not narrative importance.</p>
</aside>
""",
    },
    "hedging": {
        "kind": "article",
        "title": "Academic Hedging: Calibrate Claims to Evidence | RhetoriLex",
        "description": "Use academic hedging to express uncertainty, scope, frequency, and alternative explanations without making prose vague.",
        "h1": "Academic hedging calibrates a claim",
        "lede": "Choose a hedge for a specific evidential reason, then place it where it modifies the intended proposition.",
        "body": """
<section>
  <h2>Hedging is not automatic caution</h2>
  <p>A hedge marks a boundary in knowledge: probability, frequency, scope, measurement, design, or explanation. May indicates possibility. Tends to indicates a pattern that is not universal. In this sample limits population. Consistent with identifies compatibility without proving a mechanism. Each phrase makes a different commitment.</p>
  <p>Start by stating the strongest claim the evidence supports. Then identify the uncertain component. Modify that component rather than surrounding the whole paragraph with vague language.</p>
</section>
<section>
  <h2>Match wording to inferential force</h2>
  <p class="phrase-template">The findings indicate [descriptive result] within [scope].</p>
  <p class="phrase-template">The findings suggest that [interpretation], although [alternative explanation or limitation] cannot be excluded.</p>
  <p class="phrase-template">The results are consistent with [mechanism], but do not distinguish it from [credible alternative].</p>
  <p>Indicate is usually stronger than suggest. Consistent with expresses compatibility, not confirmation. Preserve this distinction when paraphrasing or shortening.</p>
</section>
<section>
  <h2>Remove both overstatement and needless weakness</h2>
  <p>Review each modal verb, adverb, quantifier, and scope phrase. Ask what evidence warrants it. Delete perhaps, possibly, and may when they merely cluster around an already tentative claim. Strengthen a sentence when direct evidence clearly supports it. Use <a href="{{link:preserve_claim_strength}}">Preserve Claim Strength</a> during revision.</p>
</section>
<aside class="article-note">
  <h2>Warning</h2>
  <p>A hedge cannot repair a causal claim whose design is inadequate. May cause still makes a causal proposition. Use associational language when causality is not identified.</p>
</aside>
""",
    },
    "reviewer_response": {
        "kind": "article",
        "title": "How to Write a Clear Reviewer Response | RhetoriLex",
        "description": "Write reviewer responses that identify the issue, document the revision, cite its location, and disagree with evidence when needed.",
        "h1": "A reviewer response should make revision traceable",
        "lede": "Address the substance, state what changed, point to the location, and explain the reasoning without inventing work.",
        "body": """
<section>
  <h2>Separate the comment into decisions</h2>
  <p>A reviewer comment may contain a question, requested analysis, wording issue, and broader concern. Break it into answerable points. For each point, decide whether to revise, clarify, add evidence, explain an existing choice, or disagree. Respond to the concern before describing cosmetic edits.</p>
  <p class="phrase-template">We revised [section and location] to clarify [specific issue]. The revised text now states [bounded summary of change].</p>
</section>
<section>
  <h2>Document changes precisely</h2>
  <p>Quote only the necessary revised text and provide page, line, section, table, or figure references that match the final manuscript. If an analysis was added, state the method and where the result appears. If the requested work cannot be done, explain the constraint and revise any claim affected by that limitation.</p>
  <p class="phrase-template">We agree that [shared concern] required clarification. Because [methodological reason], we did not [requested action]; instead, we [bounded revision] and now state [remaining limitation].</p>
</section>
<section>
  <h2>Disagree on methodological grounds</h2>
  <p>Professional disagreement is legitimate. Identify the point of agreement, give the evidence or design reason, and explain the manuscript change that prevents misunderstanding. Avoid appeals to preference when a verifiable standard, citation, analysis, or reporting guideline is available.</p>
  <p>Use the <a href="{{link:phrase_explorer}}?q=reviewer%20response">Phrase Explorer</a> for acknowledgement, revision, and bounded disagreement patterns.</p>
</section>
<aside class="article-note">
  <h2>Warning</h2>
  <p>Never claim that text, data, analysis, approval, or citation was added unless it appears in the submitted revision. Check every location reference after pagination changes.</p>
</aside>
""",
    },
    "association_vs_causation": {
        "kind": "article",
        "title": "Association vs Causation in Scientific Writing | RhetoriLex",
        "description": "Distinguish association from causation and choose verbs that match observational, experimental, and causal evidence.",
        "h1": "Association and causation make different claims",
        "lede": "An association describes a relation in observed data. A causal claim describes what would change under an intervention.",
        "body": """
<section>
  <h2>Identify the proposition inside the verb</h2>
  <p>Associated with, correlated with, differed, and predicted can describe statistical relations without asserting that changing one variable would change another. Caused, led to, improved, reduced, prevented, and affected usually express causal change. Temporal order and adjustment alone do not turn an association into a causal effect.</p>
  <p>Causal interpretation depends on design and assumptions: intervention or exposure definition, exchangeability, positivity, consistency, temporal order, measurement, interference, attrition, and the analysis used to estimate the target effect.</p>
</section>
<section>
  <h2>Rewrite observational overclaims</h2>
  <p class="phrase-template">In this observational analysis, exposure X was associated with outcome Y after adjustment for [measured covariates].</p>
  <p class="phrase-template">Participants with [exposure] had [difference] in outcome Y; unmeasured confounding and reverse causation remain possible.</p>
  <p>These patterns report the relation and its boundary. They do not imply that adjusting for measured variables removes every source of bias.</p>
</section>
<section>
  <h2>Use causal language only with a causal contract</h2>
  <p>State the design, target effect, identification assumptions, and relevant diagnostics. Describe violations and sensitivity analyses. Even a randomised study needs attention to adherence, missing outcomes, interference, and the estimand. Search the <a href="{{link:phrase_explorer}}?q=observational%20association">Phrase Explorer</a> and inspect the causal guard on each result.</p>
</section>
<aside class="article-note">
  <h2>Warning</h2>
  <p>Replacing causes with may cause does not remove the causal claim. If the design supports association only, change the relation itself.</p>
</aside>
""",
    },
    "preserve_claim_strength": {
        "kind": "article",
        "title": "Preserve Claim Strength When Rewriting Research | RhetoriLex",
        "description": "Preserve tentative, bounded, assertive, and causal force when paraphrasing, editing, summarising, or translating research claims.",
        "h1": "Preserve claim strength when wording changes",
        "lede": "A rewrite is faithful only when it retains what the source commits to and what it leaves uncertain.",
        "body": """
<section>
  <h2>Map the source commitment</h2>
  <p>Claim strength includes more than certainty. It combines evidence relation, modality, frequency, scope, comparison, and causal status. Suggests is not equivalent to demonstrates. In this sample is not equivalent to generally. Was associated with is not equivalent to reduced. No increase is not equivalent to a decrease.</p>
  <p>Before editing, underline the main proposition and mark every qualifier. Record citations, numbers, units, intervals, negation, direction, population, setting, time, and alternative explanations.</p>
</section>
<section>
  <h2>Use an explicit strength ladder</h2>
  <div class="move-sequence">
    <div><strong>Tentative</strong><p>The findings may reflect [interpretation].</p></div>
    <div><strong>Bounded</strong><p>Within [scope], the findings support [interpretation].</p></div>
    <div><strong>Assertive</strong><p>The analysis demonstrates [directly established result].</p></div>
    <div><strong>Causal</strong><p>Under [identified design and assumptions], exposure X changed outcome Y.</p></div>
  </div>
  <p>Do not move upward on this ladder for fluency. Moving downward can also distort a well-supported result by making it needlessly uncertain.</p>
</section>
<section>
  <h2>Verify in both directions</h2>
  <p>Ask whether the source entails the rewrite. Then ask whether the rewrite introduces any proposition the source does not entail. Compare every protected element. Use the <a href="{{link:paraphrasing}}">paraphrasing guide</a> for a full invariant checklist and search <a href="{{link:phrase_explorer}}?q=bounded%20claim">bounded claim</a> for calibrated patterns.</p>
</section>
<aside class="article-note">
  <h2>Warning</h2>
  <p>Short summaries are especially prone to strength drift because qualifications are removed first. If a limitation changes the conclusion, it is not optional detail.</p>
</aside>
""",
    },
}
