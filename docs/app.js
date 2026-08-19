"use strict";

const state = {
  patterns: [],
  visibleLimit: 12,
};

const STRENGTH_ORDER = {
  tentative: 0,
  bounded: 1,
  assertive: 2,
  causal: 3,
};

const RISK_ORDER = {
  low: 0,
  medium: 1,
  high: 2,
};

const CAUTION_INTENT_TERMS = new Set([
  "bounded",
  "careful",
  "cautious",
  "hedge",
  "hedging",
  "qualify",
  "qualified",
  "tentative",
  "uncertain",
  "uncertainty",
]);

const CAUSAL_INTENT_TERMS = new Set([
  "causal",
  "causality",
  "cause",
  "caused",
  "causes",
  "counterfactual",
  "randomised",
  "randomized",
]);

const elements = {
  form: document.querySelector("#explorer-form"),
  query: document.querySelector("#query"),
  section: document.querySelector("#section-filter"),
  functionName: document.querySelector("#function-filter"),
  strength: document.querySelector("#strength-filter"),
  status: document.querySelector("#explorer-status"),
  results: document.querySelector("#results"),
};

function asText(value) {
  if (value === null || value === undefined) return "";
  if (Array.isArray(value)) return value.map(asText).filter(Boolean).join(", ");
  if (typeof value === "object") {
    return value.label || value.name || value.level || JSON.stringify(value);
  }
  return String(value);
}

function asList(value) {
  if (Array.isArray(value)) return value.map(asText).filter(Boolean);
  const text = asText(value);
  return text ? [text] : [];
}

function humanize(value) {
  return asText(value)
    .replace(/[._-]+/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function field(pattern, ...names) {
  for (const name of names) {
    if (pattern[name] !== undefined && pattern[name] !== null) return pattern[name];
  }
  return "";
}

function normalizedField(pattern, ...names) {
  return asText(field(pattern, ...names)).trim();
}

function create(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function uniqueValues(names) {
  const values = new Set();
  for (const pattern of state.patterns) {
    const value = normalizedField(pattern, ...names);
    if (value) values.add(value);
  }
  return [...values].sort((left, right) => left.localeCompare(right));
}

function populateSelect(select, values) {
  for (const value of values) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = humanize(value);
    select.append(option);
  }
}

function searchableText(pattern) {
  return [
    field(pattern, "id"),
    field(pattern, "canonical_template", "template"),
    field(pattern, "description"),
    field(pattern, "section", "stage"),
    field(pattern, "subsection"),
    field(pattern, "function", "rhetorical_function"),
    field(pattern, "move"),
    field(pattern, "tags"),
    field(pattern, "stance"),
    field(pattern, "claim_strength"),
  ]
    .map(asText)
    .join(" ")
    .toLocaleLowerCase();
}

function scorePattern(pattern, query) {
  if (!query) return Number(field(pattern, "quality_score")) || 0;
  const haystack = searchableText(pattern);
  const normalizedQuery = query.toLocaleLowerCase().trim();
  const terms = normalizedQuery.split(/\s+/).filter(Boolean);
  let score = haystack.includes(normalizedQuery) ? 12 : 0;
  for (const term of terms) {
    if (haystack.includes(term)) score += 3;
    if (normalizedField(pattern, "function", "rhetorical_function").toLocaleLowerCase().includes(term)) score += 2;
    if (normalizedField(pattern, "section", "stage").toLocaleLowerCase().includes(term)) score += 1;
  }

  const strength = normalizedField(pattern, "claim_strength");
  const risk = normalizedField(pattern, "risk");
  const asksForCaution = terms.some((term) => CAUTION_INTENT_TERMS.has(term));
  const asksForCausality = !asksForCaution && terms.some((term) => CAUSAL_INTENT_TERMS.has(term));

  if (asksForCaution) {
    score += { tentative: 10, bounded: 6, assertive: -4, causal: -18 }[strength] || 0;
    if (risk === "high") score -= 6;
  } else if (asksForCausality && strength === "causal") {
    score += 8;
  } else if (strength === "causal") {
    score -= 3;
  }
  return score;
}

function safetyRank(pattern, fieldName, order) {
  const value = normalizedField(pattern, fieldName);
  return Object.hasOwn(order, value) ? order[value] : Number.MAX_SAFE_INTEGER;
}

function matches(pattern, query, section, functionName, strength) {
  if (section && normalizedField(pattern, "section", "stage") !== section) return false;
  if (functionName && normalizedField(pattern, "function", "rhetorical_function") !== functionName) return false;
  if (strength && normalizedField(pattern, "claim_strength") !== strength) return false;
  if (!query) return true;
  return scorePattern(pattern, query) > 0;
}

function appendCondition(container, label, value) {
  const values = asList(value);
  if (!values.length) return;
  const row = create("div", "condition");
  row.append(create("strong", "", label), create("span", "", values.join("; ")));
  container.append(row);
}

function renderResult(pattern) {
  const article = create("article", "result");
  const meta = create("div", "result-meta");
  meta.append(
    create("span", "result-id", normalizedField(pattern, "id") || "pattern"),
    create("span", "", humanize(field(pattern, "section", "stage")) || "General"),
    create("span", "", humanize(field(pattern, "function", "rhetorical_function")) || "Rhetorical move"),
  );

  const strength = normalizedField(pattern, "claim_strength");
  if (strength) meta.append(create("span", "", `Claim: ${humanize(strength)}`));

  const evidence = normalizedField(pattern, "evidence_requirement");
  if (evidence) meta.append(create("span", "", `Evidence: ${humanize(evidence)}`));

  const risk = normalizedField(pattern, "risk");
  if (risk) meta.append(create("span", "", `Risk: ${humanize(risk)}`));

  const body = create("div", "result-body");
  body.append(create("h3", "", normalizedField(pattern, "canonical_template", "template") || "Template unavailable"));

  const description = normalizedField(pattern, "description");
  if (description) body.append(create("p", "", description));

  if (field(pattern, "causal_design_required") === true) {
    appendCondition(
      body,
      "Causal guard",
      "Requires a credible causal design and explicit identifying assumptions.",
    );
  }
  appendCondition(body, "Review", field(pattern, "notes"));
  appendCondition(body, "Use when", field(pattern, "allowed_when"));
  appendCondition(body, "Avoid when", field(pattern, "avoid_when"));

  article.append(meta, body);
  return article;
}

function render() {
  const query = elements.query.value.trim();
  const section = elements.section.value;
  const functionName = elements.functionName.value;
  const strength = elements.strength.value;

  const matchesList = state.patterns
    .filter((pattern) => matches(pattern, query, section, functionName, strength))
    .map((pattern) => ({ pattern, score: scorePattern(pattern, query) }))
    .sort(
      (left, right) =>
        right.score - left.score ||
        safetyRank(left.pattern, "claim_strength", STRENGTH_ORDER) -
          safetyRank(right.pattern, "claim_strength", STRENGTH_ORDER) ||
        safetyRank(left.pattern, "risk", RISK_ORDER) - safetyRank(right.pattern, "risk", RISK_ORDER) ||
        normalizedField(left.pattern, "id").localeCompare(normalizedField(right.pattern, "id")),
    );

  elements.results.replaceChildren();
  elements.results.setAttribute("aria-busy", "false");

  if (!matchesList.length) {
    const empty = create("div", "empty-state");
    empty.append(
      create("h3", "", "No compatible pattern found"),
      create("p", "", "Broaden the intent or remove a filter. Do not force a pattern that conflicts with the evidence."),
    );
    elements.results.append(empty);
    elements.status.textContent = "0 patterns match these constraints.";
    return;
  }

  const shown = matchesList.slice(0, state.visibleLimit);
  for (const item of shown) elements.results.append(renderResult(item.pattern));

  elements.status.textContent = `${matchesList.length} compatible pattern${matchesList.length === 1 ? "" : "s"}; showing ${shown.length}.`;
}

async function loadPatterns() {
  try {
    const response = await fetch("data/phrases.json", { cache: "no-cache" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    const records = Array.isArray(payload) ? payload : payload.phrases || payload.entries || payload.patterns;
    if (!Array.isArray(records) || records.length === 0) throw new Error("No pattern records found");

    state.patterns = records;
    populateSelect(elements.section, uniqueValues(["section", "stage"]));
    populateSelect(elements.functionName, uniqueValues(["function", "rhetorical_function"]));
    populateSelect(elements.strength, uniqueValues(["claim_strength"]));
    render();
  } catch (error) {
    elements.results.setAttribute("aria-busy", "false");
    const box = create("div", "error-state");
    box.append(
      create("h3", "", "Explorer data is unavailable"),
      create("p", "", "Build deterministic data with `python scripts/build_data.py`, then serve the docs directory over HTTP."),
    );
    elements.results.replaceChildren(box);
    elements.status.textContent = "Could not load the local dataset.";
  }
}

elements.form.addEventListener("submit", (event) => {
  event.preventDefault();
  render();
});

for (const select of [elements.section, elements.functionName, elements.strength]) {
  select.addEventListener("change", render);
}

let queryTimer;
elements.query.addEventListener("input", () => {
  window.clearTimeout(queryTimer);
  queryTimer = window.setTimeout(render, 160);
});

loadPatterns();
