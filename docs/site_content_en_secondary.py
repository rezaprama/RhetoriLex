"""Additional English content for the generated RhetoriLex site."""

PAGES_EN = {
    "rhetorical_moves": {
        "kind": "article",
        "title": "Rhetorical Moves for Research Writing | RhetoriLex",
        "description": "Plan research paragraphs through rhetorical moves for context, gaps, methods, findings, interpretation, limitations, and contribution.",
        "h1": "Rhetorical moves turn a draft into an argument",
        "lede": "A move names what a passage does for the reader. Phrase choice comes after that function is clear.",
        "body": """
<section>
  <h2>Use moves as a planning layer</h2>
  <p>A rhetorical move is a communicative action such as defining a problem, positioning prior work, reporting a procedure, interpreting a finding, or limiting a conclusion. It is larger than a transition word and smaller than a whole section. Several sentences may realise one move, and one sentence may connect two moves when the relationship remains clear.</p>
  <p>Move labels help diagnose drafts. A literature review that lists studies but never compares them lacks synthesis. An introduction that announces importance but never specifies an unresolved issue lacks a defensible gap. A discussion that repeats results without explaining their relation to the question lacks interpretation.</p>
</section>
<section>
  <h2>Build a sequence that earns the claim</h2>
  <div class="move-sequence">
    <div><strong>Establish context</strong><p>Define the topic, population, or problem at the scope the paper can support.</p></div>
    <div><strong>Organise prior knowledge</strong><p>Group evidence by concept, method, result, or disagreement rather than by citation alone.</p></div>
    <div><strong>Specify the unresolved issue</strong><p>State what remains unknown, inconsistent, untested, or poorly bounded.</p></div>
    <div><strong>Present the response</strong><p>Connect the research aim and design to the issue that was established.</p></div>
    <div><strong>Interpret with limits</strong><p>Explain what the findings support and what design or evidence leaves uncertain.</p></div>
  </div>
</section>
<section>
  <h2>Test the joins between moves</h2>
  <p>Most coherence problems occur at boundaries. The evidence reviewed may not justify the stated gap. The aim may not answer the gap. The result may not support the interpretation. The conclusion may broaden the population, outcome, or causal force. Read the final sentence of one move beside the first sentence of the next and state the logical link in plain language.</p>
  <p>Do not force every paper into one template. Disciplinary conventions, study design, and genre shape which moves are expected and how visible they should be. Use the <a href="{{link:phrase_explorer}}">Phrase Explorer</a> to compare patterns only after choosing the move and its evidence constraints.</p>
</section>
<aside class="article-note">
  <h2>Paragraph audit</h2>
  <p>Label each sentence by move. If two adjacent sentences have the same function, check whether one can be removed. If a move appears without evidence or a logical bridge, repair the argument before adding transitions.</p>
</aside>
""",
    },
    "research_writing_guides": {
        "kind": "article",
        "title": "Research Writing Guides for Every Manuscript Section | RhetoriLex",
        "description": "Focused research writing guides for literature reviews, introductions, methods, results, discussions, conclusions, and reviewer responses.",
        "h1": "Research writing guides organised around decisions",
        "lede": "Choose the section you are writing, identify its main decision, and apply the checks that protect meaning.",
        "body": """
<section>
  <h2>Introduction and literature review</h2>
  <p>An introduction should narrow from a defined context to a research problem that the study can address. Avoid claiming that no research exists unless the search supports that conclusion. A useful gap is specific: a population has not been studied, methods produce inconsistent estimates, a mechanism remains uncertain, or evidence does not cover an important setting.</p>
  <p>A literature review should synthesise rather than catalogue. Group sources by question, theory, method, finding, or limitation. Make the basis of comparison explicit and ensure that a citation supports the proposition attached to it. Use <a href="{{link:academic_writing}}">Academic Writing</a> for stance and synthesis guidance.</p>
</section>
<section>
  <h2>Methods and results</h2>
  <p>Methods should document decisions needed to understand or reproduce the analysis. State the design, sample, measures, procedures, exclusions, and model choices with enough precision for the discipline. Results should report the estimate, direction, uncertainty, and relevant comparison. Keep interpretation distinguishable from observation unless the venue expects an integrated format.</p>
  <p>When a result is null or uncertain, describe what the data do and do not rule out. Do not use absence of statistical significance as proof of equivalence. See <a href="{{link:scientific_writing}}">Scientific Writing</a> for causal and design checks.</p>
</section>
<section>
  <h2>Discussion and conclusion</h2>
  <p>Begin the discussion with an answer to the research question at the strength supported by the analysis. Relate the finding to prior work, consider plausible explanations, state limitations that affect interpretation, and distinguish local implications from general claims. A conclusion should consolidate the bounded contribution rather than introduce stronger language.</p>
  <p>Use the <a href="{{link:phrase_explorer}}?q=limitation">Phrase Explorer</a> for limitation, interpretation, comparison, and contribution patterns. Review the evidence requirement on every candidate.</p>
</section>
<section>
  <h2>Reviewer responses</h2>
  <p>Respond to the substance of a comment before defending wording. State what changed, where it changed, and how the revision addresses the concern. If you disagree, identify the point of agreement, explain the methodological or conceptual reason, and offer a bounded revision where possible. Never claim to have added an analysis, citation, or result that is not present in the manuscript.</p>
</section>
<aside class="article-note">
  <h2>Final manuscript pass</h2>
  <p>Trace each major conclusion backward to a result, method, and stated question. Then trace every citation and number forward into the claim it supports. This two-way audit catches many polished but unsupported sentences.</p>
</aside>
""",
    },
    "agent_skills": {
        "kind": "article",
        "title": "RhetoriLex Agent Skill for Academic Writing | RhetoriLex",
        "description": "Install and use the RhetoriLex Agent Skill for local phrase retrieval, evidence-calibrated rewriting, and meaning-preserving paraphrase.",
        "h1": "Use RhetoriLex as an academic writing Agent Skill",
        "lede": "Retrieve original patterns locally, expose evidence constraints, and keep manuscript decisions under human control.",
        "body": """
<section>
  <h2>Install from the repository</h2>
  <p>The skill package includes instructions, a deterministic retrieval script, and the released catalog. Core search works locally and does not require manuscript upload. Review the repository and permissions before installing any agent extension.</p>
  <pre><code>$skill-installer https://github.com/rezaprama/RhetoriLex/tree/main/skills/rhetorilex</code></pre>
  <p>You can also clone the repository and point your agent to <code>skills/rhetorilex/SKILL.md</code>. The Python command-line interface supports the same catalog for reproducible searches.</p>
</section>
<section>
  <h2>Ask for purpose and constraints</h2>
  <p>A useful prompt names the rhetorical task, manuscript section, evidence type, and protected meaning. It also tells the agent what it must not infer. These examples are starting points:</p>
  <div class="prompt-list">
    <div><strong>Observational rewrite</strong><p><code>Rewrite this observational result without causal language. Preserve the estimate, interval, population, and citation. Explain any wording that would require a causal design.</code></p></div>
    <div><strong>Meaning preservation</strong><p><code>Paraphrase this sentence. Preserve citation, number, unit, negation, comparison direction, and uncertainty. Return a checklist showing each invariant.</code></p></div>
    <div><strong>Pattern retrieval</strong><p><code>Find three patterns for a cautious discussion interpretation. Prefer tentative or bounded claim strength and low risk. Show evidence requirements before the templates.</code></p></div>
  </div>
</section>
<section>
  <h2>Read the output as a proposal</h2>
  <p>The agent should identify the move, return candidate patterns, explain claim strength, and warn when evidence does not meet a requirement. It should not invent results, references, methods, or consensus. A causal pattern is not permission to make a causal claim. The design and identifying assumptions must already justify it.</p>
  <p>After adapting a pattern, compare the sentence with the manuscript evidence. Verify names, citations, numbers, units, direction, negation, modality, population, time, and limitations. Ask a subject specialist when interpretation depends on domain knowledge.</p>
</section>
<section>
  <h2>Keep searches reproducible</h2>
  <p>Record the catalog version or commit, query, filters, and selected pattern ID when the wording decision matters. The command-line interface can return stable IDs for this purpose. Search is deterministic, so the same catalog and query produce an auditable result order.</p>
  <pre><code>rhetorilex search "cautious interpretation" --limit 3
rhetorilex show RLX-DISCUSS-INTERPRET-001</code></pre>
</section>
<aside class="article-note">
  <h2>Privacy boundary</h2>
  <p>Local retrieval does not send manuscript text anywhere. The surrounding agent or model may have different data practices. Check that system separately before providing confidential, embargoed, or personally identifiable material.</p>
</aside>
""",
    },
    "about": {
        "kind": "article",
        "title": "About RhetoriLex: Originality, Provenance, and Licensing",
        "description": "Learn how RhetoriLex maintains an original clean-room academic phrase catalog, evidence safeguards, open licensing, and project governance.",
        "h1": "RhetoriLex is an original rhetorical pattern index",
        "lede": "The project helps writers choose language by purpose and evidence without redistributing restricted phrasebank content.",
        "body": """
<section>
  <h2>What the project provides</h2>
  <p>RhetoriLex is a structured catalog of independently authored English patterns for academic and scientific writing. Each record links a rhetorical function to a template, manuscript stage, claim strength, evidence requirement, risk level, and review notes. The web explorer, Python interface, command-line tool, and Agent Skill consume the same released data.</p>
  <p>The catalog is a writing aid, not an authority on whether a scientific claim is true. Writers remain responsible for source accuracy, disciplinary conventions, research integrity, and the fit between wording and evidence.</p>
</section>
<section>
  <h2>Clean-room authorship and provenance</h2>
  <p>Released patterns are original editorial work. Restricted local source inventories are excluded from the repository and release artifacts. The project does not import, reproduce, or lightly rewrite the Manchester Academic Phrasebank inventory. External resources may inform concepts, taxonomy, or aggregate validation only when their role and license are documented.</p>
  <p>Build checks scan tracked and packaged content for restricted filenames and other leakage indicators. Provenance records state what was considered, what was excluded, and why. Read the complete <a href="https://github.com/rezaprama/RhetoriLex/blob/main/PROVENANCE.md">provenance policy</a> before proposing a new corpus source.</p>
</section>
<section>
  <h2>Licensing and attribution</h2>
  <p>Original editorial data and human-facing documentation are released under Creative Commons Attribution 4.0. Software and Agent Skill instructions are released under Apache License 2.0. Third-party material, if accepted in the future, must retain its own notice and may not be covered by either project license.</p>
  <p>Created by Reza Prama Arviandi. Contributors are credited through repository history and release records. See the <a href="https://github.com/rezaprama/RhetoriLex/blob/main/LICENSE">software license</a>, <a href="https://github.com/rezaprama/RhetoriLex/blob/main/LICENSES/CC-BY-4.0.txt">data license</a>, and <a href="https://github.com/rezaprama/RhetoriLex/blob/main/GOVERNANCE.md">governance policy</a>.</p>
</section>
<section>
  <h2>How to contribute responsibly</h2>
  <p>Propose a rhetorical need, evidence contract, and original wording. Do not contribute phrases copied from restricted sources or manuscripts without authorisation. Tests check schema validity, deterministic builds, safety semantics, and provenance metadata. Editorial review checks whether a pattern is useful, distinct, natural, and calibrated to its evidence requirement.</p>
  <p>Use the repository issue tracker for defects, taxonomy proposals, accessibility reports, and documentation improvements. Report security concerns through the documented private channel rather than a public issue.</p>
</section>
<aside class="article-note">
  <h2>Scope</h2>
  <p>RhetoriLex does not generate evidence, verify every citation, replace domain review, or guarantee publication. It makes wording decisions more explicit and auditable.</p>
</aside>
""",
    },
}
