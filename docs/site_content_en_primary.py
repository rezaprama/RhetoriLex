"""English content for the generated RhetoriLex site."""

PAGES_EN = {
    "home": {
        "kind": "home",
        "title": "Free Local Academic Paraphrase Skill | RhetoriLex",
        "description": "Use a free local-first academic paraphrase skill and web workbench for evidence-safe rewriting, Indonesian-friendly support, and original writing patterns.",
        "h1": "Free local academic paraphrase skill for researchers.",
        "lede": "Paraphrase, audit, and revise academic, scientific, technical, and Indonesian-English writing with local-first controls, explicit evidence checks, and no paid SaaS requirement.",
        "body": """
<section class="section-block" aria-labelledby="purpose-index-title">
  <div class="section-heading">
    <h2 id="purpose-index-title">Start with the writing problem</h2>
    <p>Choose a paraphrase, audit, writing, or revision task. RhetoriLex links purpose, evidence, protected meaning, and final checks.</p>
  </div>
  <ul class="purpose-index">
    <li><a href="{{link:paraphrase_workbench}}"><strong>Paraphrase Workbench</strong><span>Installable local-first tool with your own endpoint, token, or local model.</span></a></li>
    <li><a href="{{link:academic_writing}}"><strong>Academic Writing</strong><span>Build arguments, syntheses, transitions, and bounded conclusions.</span></a></li>
    <li><a href="{{link:scientific_writing}}"><strong>Scientific Writing</strong><span>Report methods, results, uncertainty, and causal limits precisely.</span></a></li>
    <li><a href="{{link:phrase_explorer}}"><strong>Phrase Explorer</strong><span>Search the original catalog in natural language and filter by evidence.</span></a></li>
    <li><a href="{{link:paraphrasing}}"><strong>Paraphrasing</strong><span>Preserve citations, numbers, negation, scope, and inferential force.</span></a></li>
    <li><a href="{{link:rhetorical_moves}}"><strong>Rhetorical Moves</strong><span>Plan what a paragraph does before choosing how it sounds.</span></a></li>
    <li><a href="{{link:research_writing_guides}}"><strong>Research Writing Guides</strong><span>Use focused guidance for reviews, methods, results, and discussions.</span></a></li>
    <li><a href="{{link:agent_skills}}"><strong>Agent Skills</strong><span>Use RhetoriLex in a local agent workflow with explicit safety checks.</span></a></li>
    <li><a href="{{link:about}}"><strong>About</strong><span>Read the clean-room, authorship, licensing, and governance record.</span></a></li>
  </ul>
</section>
<section class="section-block" aria-labelledby="popular-moves-title">
  <div class="section-heading">
    <h2 id="popular-moves-title">Popular writing tasks</h2>
    <p>Open a focused guide when the sentence problem is already clear.</p>
  </div>
  <ul class="compact-link-index">
    <li><a href="{{link:research_gap}}"><strong>Establish a research gap</strong><span>Define a specific unresolved issue without claiming that no research exists.</span></a></li>
    <li><a href="{{link:literature_review}}"><strong>Synthesise literature</strong><span>Compare evidence on an explicit analytical basis.</span></a></li>
    <li><a href="{{link:hedging}}"><strong>Calibrate uncertainty</strong><span>Choose hedging that marks a real evidential boundary.</span></a></li>
    <li><a href="{{link:association_vs_causation}}"><strong>Separate association from causation</strong><span>Use relations that the study design can support.</span></a></li>
    <li><a href="{{link:reviewer_response}}"><strong>Respond to a reviewer</strong><span>Make every answer and revision traceable.</span></a></li>
    <li><a href="{{link:preserve_claim_strength}}"><strong>Preserve claim strength</strong><span>Protect inferential force when editing or paraphrasing.</span></a></li>
  </ul>
</section>
<section class="section-block" aria-labelledby="paper-section-title">
  <div class="section-heading">
    <h2 id="paper-section-title">Browse by paper section</h2>
    <p>Use section guidance when you know where the sentence belongs but not which move it needs.</p>
  </div>
  <nav class="section-links" aria-label="Paper sections">
    <a href="{{link:research_gap}}">Introduction</a>
    <a href="{{link:literature_review}}">Literature review</a>
    <a href="{{link:methods}}">Methods</a>
    <a href="{{link:results}}">Results</a>
    <a href="{{link:discussion}}">Discussion</a>
    <a href="{{link:thesis}}">Thesis</a>
  </nav>
</section>
<section class="section-block comparison-block" aria-labelledby="evidence-title">
  <div class="section-heading">
    <h2 id="evidence-title">Style follows evidence</h2>
    <p>A fluent sentence can still misstate the study. Calibrate the relation before polishing the prose.</p>
  </div>
  <div class="comparison-lines">
    <div><strong>Unsupported causal claim</strong><p>Our observational analysis proves that exposure X causes outcome Y.</p></div>
    <div><strong>Evidence-calibrated claim</strong><p>In this observational analysis, exposure X was associated with outcome Y.</p></div>
  </div>
</section>
<section class="section-block install-block" aria-labelledby="install-home-title">
  <div>
    <h2 id="install-home-title">Free, local, installable</h2>
    <p>Open the workbench, download the released JSON catalog, review clean-room provenance, or install the local Agent Skill.</p>
  </div>
  <pre><code>$skill-installer https://github.com/rezaprama/RhetoriLex/tree/main/skills/rhetorilex</code></pre>
  <ul class="resource-links">
    <li><a href="{{link:paraphrase_workbench}}">Open Paraphrase Workbench</a></li>
    <li><a href="https://rezaprama.github.io/RhetoriLex/data/phrases.json">Open dataset</a></li>
    <li><a href="https://github.com/rezaprama/RhetoriLex/blob/main/PROVENANCE.md">Read methodology and provenance</a></li>
    <li><a href="{{link:agent_skills}}">Read installation and prompt examples</a></li>
  </ul>
</section>
""",
    },
    "academic_writing": {
        "kind": "article",
        "title": "Academic Writing: Purpose, Structure, and Evidence | RhetoriLex",
        "description": "A practical guide to academic writing by rhetorical purpose, with paragraph moves, stance control, synthesis, and revision checks.",
        "h1": "Academic writing begins with rhetorical purpose",
        "lede": "Plan what each sentence must accomplish, then choose language that matches the evidence and argument.",
        "body": """
<section>
  <h2>Move from task to rhetorical function</h2>
  <p>Academic writing is easier to revise when every sentence has a job. A literature review may define a field, organise positions, compare findings, identify uncertainty, or establish a research gap. A discussion may interpret a result, connect it to prior work, bound its scope, and explain an implication. These functions are related, but they are not interchangeable.</p>
  <p>Before drafting, write a plain-language label beside each paragraph: context, problem, evidence, interpretation, limitation, or contribution. If a paragraph needs three labels, its logic may need to be separated. Once the sequence is clear, use the <a href="{{link:phrase_explorer}}">Phrase Explorer</a> to find a pattern for the specific move.</p>
</section>
<section>
  <h2>Control stance across a paragraph</h2>
  <p>Stance is not a single hedge added near a verb. It is the relation among evidence quality, claim strength, scope, and certainty. Direct evidence can support an assertive descriptive claim. Observational evidence can support association, but it normally cannot support an unqualified causal statement. Contextual evidence may motivate a question without resolving it.</p>
  <div class="reference-table" role="region" aria-label="Academic writing decisions" tabindex="0">
    <table>
      <thead><tr><th>Writing need</th><th>Useful move</th><th>Check before use</th></tr></thead>
      <tbody>
        <tr><td>Connect studies</td><td>Synthesise agreement and contrast</td><td>Do the cited studies support the same scope?</td></tr>
        <tr><td>State a gap</td><td>Define the unresolved issue</td><td>Is the gap specific and demonstrable?</td></tr>
        <tr><td>Interpret a result</td><td>Offer a bounded explanation</td><td>Could another mechanism fit the evidence?</td></tr>
        <tr><td>Conclude</td><td>Return to contribution and limits</td><td>Does the conclusion exceed the analysis?</td></tr>
      </tbody>
    </table>
  </div>
</section>
<section>
  <h2>Revise for continuity and precision</h2>
  <p>Read the first sentence of every paragraph as a sequence. The sequence should reveal the paper's argument without relying on formulaic transitions. Then inspect each claim for its evidence anchor. A citation must still support the same proposition after a rewrite. A number must retain its unit, comparison group, interval, and direction. Negation and limiting words such as only, may, within, and under should be treated as protected meaning.</p>
  <p>Finish with a compression pass. Remove phrases that repeat the claim without adding logic. Prefer a precise subject and verb over abstract nominalisations when the actor or process matters. Keep technical terms when a shorter synonym would change disciplinary meaning.</p>
</section>
<aside class="article-note">
  <h2>Quick revision check</h2>
  <p>Can you name the move, point to its evidence, state its scope, and explain why its level of certainty is justified? If not, revise the reasoning before the wording.</p>
</aside>
""",
    },
    "scientific_writing": {
        "kind": "article",
        "title": "Scientific Writing: Methods, Results, and Causal Limits | RhetoriLex",
        "description": "Write scientific methods, results, and interpretations with explicit design, uncertainty, effect size, and causal safeguards.",
        "h1": "Scientific writing connects language to study design",
        "lede": "Report what was measured, estimated, and supported without letting polished prose outrun the analysis.",
        "body": """
<section>
  <h2>Keep methods reproducible and claims traceable</h2>
  <p>A methods section should let a qualified reader understand the population, materials, variables, procedures, exclusions, estimand, and analysis. Name choices that affect interpretation. Passive voice can be useful when the procedure matters more than the actor, but it should not hide who made a judgment or how a classification was assigned.</p>
  <p>Link every reported estimate to the corresponding method. If a model changes across analyses, state the adjustment set and purpose. If missing data, multiplicity, measurement error, or sensitivity analysis affects the result, report it where readers can connect the issue to the estimate.</p>
</section>
<section>
  <h2>Separate observation from interpretation</h2>
  <p>Results sections should report direction, magnitude, uncertainty, and the comparison being made. Statistical significance alone is not an interpretation of practical or scientific importance. Give the estimate and interval where appropriate, preserve units, and avoid translating a non-significant result into proof of no effect.</p>
  <div class="reference-table" role="region" aria-label="Scientific section responsibilities" tabindex="0">
    <table>
      <thead><tr><th>Section</th><th>Primary responsibility</th><th>Common risk</th></tr></thead>
      <tbody>
        <tr><td>Methods</td><td>Describe design and analytic decisions</td><td>Omitting choices that shape the estimand</td></tr>
        <tr><td>Results</td><td>Report estimates and uncertainty</td><td>Replacing magnitude with significance labels</td></tr>
        <tr><td>Discussion</td><td>Interpret within design limits</td><td>Presenting an association as a cause</td></tr>
        <tr><td>Conclusion</td><td>State the bounded contribution</td><td>Generalising beyond population or setting</td></tr>
      </tbody>
    </table>
  </div>
</section>
<section>
  <h2>Treat causal language as a design claim</h2>
  <p>Words such as caused, led to, reduced, improved, and prevented make claims about counterfactual change. They require more than a strong association. A credible causal statement depends on design, identification assumptions, temporal ordering, confounding control, measurement, and analysis. When those conditions are not met, use descriptive or associational language and state the remaining uncertainty.</p>
  <p>Search terms such as <a href="{{link:phrase_explorer}}?q=cautious%20interpretation">cautious interpretation</a> or <a href="{{link:phrase_explorer}}?q=observational%20association">observational association</a> surface patterns whose evidence requirements can be checked before use.</p>
</section>
<aside class="article-note">
  <h2>Before submission</h2>
  <p>Cross-check every number against the analysis output, every table reference against the final layout, and every causal verb against the study design. Ask a domain expert to review claims whose interpretation depends on specialised assumptions.</p>
</aside>
""",
    },
    "phrase_explorer": {
        "kind": "explorer",
        "title": "Academic Phrase Explorer by Rhetorical Intent | RhetoriLex",
        "description": "Search original academic English patterns by natural-language intent, section, function, claim strength, evidence requirement, and risk.",
        "h1": "Find an academic phrase by rhetorical intent",
        "lede": "Describe the work your sentence must do. Results expose evidence requirements and claim risk before you copy a pattern.",
        "body": """
<section class="explainer-grid" aria-labelledby="read-entry-title">
  <div>
    <h2 id="read-entry-title">How to read a phrase reference</h2>
    <p>The template is a starting structure, not a sentence to paste unchanged. The function identifies its rhetorical job. Claim strength and evidence requirement indicate what must be true before the wording is defensible. Notes and causal guards identify conditions that need human review.</p>
  </div>
  <div>
    <h2>Adapt, then verify</h2>
    <p>Replace every placeholder with manuscript-specific content. Compare the result with the source claim and evidence. Preserve citations, numbers, units, negation, comparison direction, population, time, and uncertainty. Copying a pattern does not transfer support from another study.</p>
  </div>
</section>
<section class="reference-anatomy" aria-labelledby="anatomy-title">
  <h2 id="anatomy-title">Reference entry anatomy</h2>
  <article class="phrase-entry static-entry">
    <div class="entry-meta"><code>EXAMPLE-BOUNDING</code><span>Discussion</span><span>Tentative claim</span></div>
    <h3>Bound an interpretation</h3>
    <p class="phrase-template">Taken together, these findings suggest that [bounded interpretation], although [limitation] constrains conclusions about [scope].</p>
    <button class="copy-button" type="button" data-copy-value="Taken together, these findings suggest that [bounded interpretation], although [limitation] constrains conclusions about [scope].">Copy pattern</button>
    <dl class="entry-facts"><div><dt>Evidence requirement</dt><dd>Convergent</dd></div><div><dt>Risk</dt><dd>Low when the limitation is explicit</dd></div><div><dt>Causal guard</dt><dd>Not required for this tentative pattern</dd></div></dl>
  </article>
</section>
""",
    },
    "paraphrasing": {
        "kind": "article",
        "title": "Academic Paraphrasing Without Meaning Drift | RhetoriLex",
        "description": "Paraphrase academic prose while preserving citations, numbers, units, negation, scope, comparison direction, and uncertainty.",
        "h1": "Paraphrasing is a meaning-preservation task",
        "lede": "Change wording only after identifying the facts, logic, scope, and inferential force that must remain invariant.",
        "body": """
<section>
  <h2>Protect meaning before changing form</h2>
  <p>A successful paraphrase is not measured by synonym count or surface difference. It is measured by whether the rewritten sentence makes the same supported claim. Begin by marking protected elements: citations, names, numbers, units, intervals, technical terms, negation, comparison direction, population, setting, time, modality, and causal status.</p>
  <p>Consider this source statement: Study A reported no increase in outcome Y after 12 weeks (Lee, 2024). A safe rewrite must retain the negative finding, the outcome, the 12-week period, and the citation. Changing no increase to reduced, or omitting the time period, changes the claim.</p>
</section>
<section>
  <h2>Use a constraint-first workflow</h2>
  <ol class="workflow-list compact">
    <li><strong>Extract invariants</strong><span>List evidence, numbers, relations, and qualifying terms that cannot change.</span></li>
    <li><strong>State the proposition plainly</strong><span>Write the supported meaning without trying to sound polished.</span></li>
    <li><strong>Rebuild the sentence</strong><span>Change structure and emphasis while retaining disciplinary terms that carry exact meaning.</span></li>
    <li><strong>Run a bidirectional check</strong><span>Ask whether the source entails the rewrite and whether the rewrite adds any unsupported proposition.</span></li>
  </ol>
</section>
<section>
  <h2>Watch for quiet forms of drift</h2>
  <p>Meaning often changes through small edits. May becomes will. Associated with becomes led to. Some participants becomes participants. Higher than becomes different from. A result limited to one setting becomes a general claim. A citation moves to a sentence containing a new proposition it did not support.</p>
  <p>When a passage is already concise, highly technical, or legally fixed, paraphrasing may be the wrong goal. Quote briefly when quotation is justified and permitted, cite the source, or retain the technical wording while rewriting the surrounding explanation. Never paraphrase to conceal dependence on a source.</p>
</section>
<aside class="article-note">
  <h2>Use RhetoriLex safely</h2>
  <p>Ask the Agent Skill to protect a citation, number, and negation explicitly. Then verify the output against the source yourself. See <a href="{{link:agent_skills}}">Agent Skills</a> for prompt patterns.</p>
</aside>
""",
    },
    "paraphrase_workbench": {
        "kind": "workbench",
        "title": "Free Local Paraphrase Workbench | RhetoriLex",
        "description": "Use an installable local-first paraphrase workbench with your own OpenAI-compatible endpoint, browser-side daily limits, and evidence checks.",
        "h1": "Free local paraphrase workbench.",
        "lede": "Use your own AI endpoint or local model to rewrite academic, scientific, technical, and Indonesian-English writing while preserving evidence and meaning.",
        "body": """
<section>
  <h2>Why local-first matters</h2>
  <p>Many paraphrase services ask writers to paste drafts into a remote form and pay for stronger limits. RhetoriLex takes a different route. The public app is static, installable, and free. It can build a safe prompt without any endpoint, or call only the OpenAI-compatible endpoint that the user enters.</p>
  <p>This keeps the default tool useful for researchers, students, supervisors, editors, and Indonesian writers who need careful English without turning every sentence into a paid request. The app does not store manuscripts on a RhetoriLex server because the current web version has no server-side manuscript database.</p>
</section>
<section>
  <h2>Safe setup choices</h2>
  <div class="reference-table" role="region" aria-label="Paraphrase workbench setup choices" tabindex="0">
    <table>
      <thead><tr><th>Choice</th><th>How it works</th><th>Privacy check</th></tr></thead>
      <tbody>
        <tr><td>Prompt only</td><td>RhetoriLex builds the instruction and invariant checklist.</td><td>No AI call leaves the browser.</td></tr>
        <tr><td>Local endpoint</td><td>Use an OpenAI-compatible local server such as a local model gateway.</td><td>Keep endpoint on your own machine or network.</td></tr>
        <tr><td>Provider endpoint</td><td>Enter your own endpoint, model, and token when your provider permits browser calls.</td><td>Your text goes to that provider, not to RhetoriLex.</td></tr>
      </tbody>
    </table>
  </div>
</section>
<section>
  <h2>Why the hosted web limit is local</h2>
  <p>The public page applies a three-call daily guard in browser storage. This is a courtesy limit, not account security. It prevents accidental overuse while keeping the static site free and deployable on GitHub Pages.</p>
  <p>A true shared-key hosted service needs a backend. The planned design is a small Worker API, a D1 table for anonymous daily quota, a KV cache for rate-limit decisions, Turnstile for abuse resistance, provider tokens stored only as server secrets, and manuscript logging disabled by default. That backend is intentionally separate from the current static app.</p>
</section>
<aside class="article-note">
  <h2>Use the result as a draft</h2>
  <p>Always compare output with the source. Verify citations, numbers, terms, negation, uncertainty, claim strength, and journal or university rules before submission.</p>
</aside>
""",
    },
}
