"use strict";

const THEME_KEY = "rhetorilex.theme";
const LOCALE_KEY = "rhetorilex.locale";
const VALID_THEMES = new Set(["system", "light", "dark"]);

function readPreference(key) {
  try {
    return window.localStorage.getItem(key);
  } catch (error) {
    return null;
  }
}

function writePreference(key, value) {
  try {
    window.localStorage.setItem(key, value);
  } catch (error) {
    return;
  }
}

function applyTheme(preference) {
  const selected = VALID_THEMES.has(preference) ? preference : "system";
  const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const dark = selected === "dark" || (selected === "system" && systemDark);
  document.documentElement.dataset.theme = dark ? "dark" : "light";
  document.documentElement.dataset.themePreference = selected;
  const themeMeta = document.querySelector("[data-theme-color]");
  if (themeMeta) themeMeta.setAttribute("content", dark ? "#10161e" : "#f5f3ed");
  for (const control of document.querySelectorAll("[data-theme-control]")) {
    control.value = selected;
  }
}

const initialTheme = readPreference(THEME_KEY) || document.documentElement.dataset.themePreference || "system";
applyTheme(initialTheme);

for (const control of document.querySelectorAll("[data-theme-control]")) {
  control.addEventListener("change", () => {
    const preference = VALID_THEMES.has(control.value) ? control.value : "system";
    writePreference(THEME_KEY, preference);
    applyTheme(preference);
  });
}

const colorScheme = window.matchMedia("(prefers-color-scheme: dark)");
colorScheme.addEventListener("change", () => {
  if ((readPreference(THEME_KEY) || "system") === "system") applyTheme("system");
});

const pageLocale = document.documentElement.lang;
if (pageLocale === "en" || pageLocale === "id") writePreference(LOCALE_KEY, pageLocale);

for (const link of document.querySelectorAll("[data-locale-link]")) {
  link.addEventListener("click", () => {
    const locale = link.dataset.localeLink;
    if (locale === "en" || locale === "id") writePreference(LOCALE_KEY, locale);
  });
}

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  for (const menu of document.querySelectorAll(".index-menu[open]")) menu.removeAttribute("open");
});

async function copyText(value) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(value);
    return;
  }
  const fallback = document.createElement("textarea");
  fallback.value = value;
  fallback.setAttribute("readonly", "");
  fallback.style.position = "fixed";
  fallback.style.left = "-100vw";
  document.body.append(fallback);
  fallback.select();
  const copied = document.execCommand("copy");
  fallback.remove();
  if (!copied) throw new Error("Copy command failed");
}

document.addEventListener("click", async (event) => {
  const button = event.target.closest("button[data-copy-value]");
  if (!button) return;
  const locale = document.documentElement.lang === "id" ? "id" : "en";
  const status = document.querySelector("#copy-status");
  const originalLabel = button.dataset.copyLabel || button.textContent;
  button.dataset.copyLabel = originalLabel;
  try {
    await copyText(button.dataset.copyValue || "");
    button.textContent = locale === "id" ? "Tersalin" : "Copied";
    if (status) status.textContent = locale === "id" ? "Pola disalin ke clipboard." : "Pattern copied to clipboard.";
  } catch (error) {
    button.textContent = originalLabel;
    if (status) {
      status.textContent =
        locale === "id"
          ? "Penyalinan otomatis gagal. Pilih dan salin teks secara manual."
          : "Automatic copy failed. Select and copy the text manually.";
    }
    return;
  }
  window.setTimeout(() => {
    button.textContent = originalLabel;
  }, 1600);
});

const explorer = document.querySelector("[data-explorer]");

if (explorer) {
  const locale = explorer.dataset.locale === "id" ? "id" : "en";
  const state = {
    patterns: [],
    visibleLimit: 20,
    matches: [],
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

  const QUERY_ALIASES = new Map([
    ["asosiasi", "association"],
    ["batasan", "limitation"],
    ["berhati-hati", "cautious"],
    ["diskusi", "discussion"],
    ["hasil", "results"],
    ["hati-hati", "cautious"],
    ["interpretasi", "interpretation"],
    ["kausal", "causal"],
    ["kesenjangan", "gap"],
    ["keterbatasan", "limitation"],
    ["ketidakpastian", "uncertainty"],
    ["literatur", "literature"],
    ["membandingkan", "compare"],
    ["metode", "methods"],
    ["observasional", "observational"],
    ["pendahuluan", "introduction"],
    ["perbandingan", "comparison"],
    ["simpulan", "conclusion"],
    ["temuan", "findings"],
  ]);

  const TEXT = {
    en: {
      pattern: "Rhetorical pattern",
      general: "General",
      copy: "Copy pattern",
      evidence: "Evidence requirement",
      strength: "Claim strength",
      risk: "Risk",
      causal: "Causal guard",
      causalText: "Requires a credible causal design and explicit identifying assumptions.",
      notes: "Review notes",
      disciplines: "Disciplines",
      useWhen: "Use when",
      avoidWhen: "Avoid when",
      emptyTitle: "No compatible pattern found",
      emptyText: "Broaden the intent or remove a filter. Do not force a pattern that conflicts with the evidence.",
      unavailableTitle: "Explorer data is unavailable",
      unavailableText: "Build the deterministic catalog, then serve the docs directory over HTTP. The local CLI remains available.",
      zero: "0 patterns match these constraints.",
      count: (total, shown) =>
        total + " compatible pattern" + (total === 1 ? "" : "s") + "; showing " + shown + ".",
    },
    id: {
      pattern: "Pola retoris",
      general: "Umum",
      copy: "Salin pola",
      evidence: "Kebutuhan bukti",
      strength: "Kekuatan klaim",
      risk: "Risiko",
      causal: "Pengaman kausal",
      causalText: "Memerlukan desain kausal yang kredibel dan asumsi identifikasi yang eksplisit.",
      notes: "Catatan tinjauan",
      disciplines: "Disiplin",
      useWhen: "Gunakan ketika",
      avoidWhen: "Hindari ketika",
      emptyTitle: "Tidak ada pola yang kompatibel",
      emptyText: "Perluas tujuan atau hapus filter. Jangan memaksa pola yang bertentangan dengan bukti.",
      unavailableTitle: "Data penjelajah tidak tersedia",
      unavailableText: "Bangun katalog deterministik, lalu sajikan direktori docs melalui HTTP. CLI lokal tetap tersedia.",
      zero: "0 pola sesuai dengan batasan ini.",
      count: (total, shown) => total + " pola kompatibel; menampilkan " + shown + ".",
    },
  }[locale];

  const elements = {
    form: document.querySelector("#explorer-form"),
    query: document.querySelector("#query"),
    stage: document.querySelector("#section-filter"),
    functionName: document.querySelector("#function-filter"),
    strength: document.querySelector("#strength-filter"),
    evidence: document.querySelector("#evidence-filter"),
    risk: document.querySelector("#risk-filter"),
    clear: document.querySelector("#clear-search"),
    status: document.querySelector("#explorer-status"),
    results: document.querySelector("#results"),
    showMore: document.querySelector("#show-more"),
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

  function field(pattern, ...names) {
    for (const name of names) {
      if (pattern[name] !== undefined && pattern[name] !== null) return pattern[name];
    }
    return "";
  }

  function normalizedField(pattern, ...names) {
    return asText(field(pattern, ...names)).trim();
  }

  function humanize(value) {
    return asText(value)
      .replace(/[._-]+/g, " ")
      .replace(/\b\w/g, (letter) => letter.toUpperCase());
  }

  function create(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function translatedQuery(value) {
    let query = value.toLocaleLowerCase().trim();
    if (locale !== "id") return query;
    for (const [source, destination] of QUERY_ALIASES) {
      query = query.split(source).join(destination);
    }
    return query;
  }

  function searchableText(pattern) {
    return [
      field(pattern, "id"),
      field(pattern, "title"),
      field(pattern, "canonical_template", "template"),
      field(pattern, "description"),
      field(pattern, "section", "stage"),
      field(pattern, "subsection"),
      field(pattern, "function", "rhetorical_function"),
      field(pattern, "move"),
      field(pattern, "keywords", "tags"),
      field(pattern, "stance"),
      field(pattern, "claim_strength"),
      field(pattern, "evidence_requirement"),
      field(pattern, "notes"),
    ]
      .map(asText)
      .join(" ")
      .toLocaleLowerCase();
  }

  function scorePattern(pattern, query) {
    if (!query) return Number(field(pattern, "quality_score")) || 0;
    const haystack = searchableText(pattern);
    const normalizedQuery = translatedQuery(query);
    const terms = normalizedQuery.split(/\s+/).filter(Boolean);
    let matchedTerms = 0;
    let score = haystack.includes(normalizedQuery) ? 14 : 0;

    for (const term of terms) {
      if (haystack.includes(term)) {
        score += 3;
        matchedTerms += 1;
      }
      if (normalizedField(pattern, "function", "rhetorical_function").toLocaleLowerCase().includes(term)) score += 3;
      if (normalizedField(pattern, "title").toLocaleLowerCase().includes(term)) score += 2;
      if (normalizedField(pattern, "section", "stage").toLocaleLowerCase().includes(term)) score += 1;
    }

    if (!matchedTerms) return 0;
    score += (matchedTerms / terms.length) * 8;

    const strength = normalizedField(pattern, "claim_strength").toLocaleLowerCase();
    const risk = normalizedField(pattern, "risk").toLocaleLowerCase();
    const asksForCaution = terms.some((term) => CAUTION_INTENT_TERMS.has(term));
    const asksForCausality = !asksForCaution && terms.some((term) => CAUSAL_INTENT_TERMS.has(term));

    if (asksForCaution) {
      score += { tentative: 10, bounded: 6, assertive: -4, causal: -18 }[strength] || 0;
      if (risk === "high") score -= 7;
    } else if (asksForCausality && strength === "causal") {
      score += 8;
    } else if (strength === "causal") {
      score -= 3;
    }
    return score;
  }

  function safetyRank(pattern, fieldName, order) {
    const value = normalizedField(pattern, fieldName).toLocaleLowerCase();
    return Object.hasOwn(order, value) ? order[value] : Number.MAX_SAFE_INTEGER;
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

  function matchesFilters(pattern) {
    if (elements.stage.value && normalizedField(pattern, "section", "stage") !== elements.stage.value) return false;
    if (
      elements.functionName.value &&
      normalizedField(pattern, "function", "rhetorical_function") !== elements.functionName.value
    ) {
      return false;
    }
    if (elements.strength.value && normalizedField(pattern, "claim_strength") !== elements.strength.value) return false;
    if (
      elements.evidence.value &&
      normalizedField(pattern, "evidence_requirement") !== elements.evidence.value
    ) {
      return false;
    }
    if (elements.risk.value && normalizedField(pattern, "risk") !== elements.risk.value) return false;
    const query = elements.query.value.trim();
    return !query || scorePattern(pattern, query) > 0;
  }

  function appendFact(container, label, value) {
    const text = asText(value).trim();
    if (!text) return;
    const wrapper = create("div");
    wrapper.append(create("dt", "", label), create("dd", "", humanize(text)));
    container.append(wrapper);
  }

  function appendCondition(container, label, value) {
    const values = asList(value);
    if (!values.length) return;
    const row = create("div", "entry-condition");
    row.append(create("strong", "", label), create("span", "", values.join("; ")));
    container.append(row);
  }

  function renderResult(pattern) {
    const article = create("article", "phrase-entry");
    const meta = create("div", "entry-meta");
    meta.append(
      create("code", "result-id", normalizedField(pattern, "id") || "pattern"),
      create("span", "", humanize(field(pattern, "section", "stage")) || TEXT.general),
      create("span", "", humanize(field(pattern, "function", "rhetorical_function")) || TEXT.pattern),
    );

    const content = create("div", "entry-content");
    content.append(create("h3", "", normalizedField(pattern, "title") || TEXT.pattern));

    const template = normalizedField(pattern, "canonical_template", "template");
    content.append(create("p", "phrase-template", template || TEXT.pattern));

    if (template) {
      const copy = create("button", "copy-button", TEXT.copy);
      copy.type = "button";
      copy.dataset.copyValue = template;
      content.append(copy);
    }

    const description = normalizedField(pattern, "description");
    if (description) content.append(create("p", "entry-description", description));

    const facts = create("dl", "entry-facts");
    appendFact(facts, TEXT.evidence, field(pattern, "evidence_requirement"));
    appendFact(facts, TEXT.strength, field(pattern, "claim_strength"));
    appendFact(facts, TEXT.risk, field(pattern, "risk"));
    if (facts.children.length) content.append(facts);

    if (field(pattern, "causal_design_required") === true) {
      appendCondition(content, TEXT.causal, TEXT.causalText);
    }
    appendCondition(content, TEXT.notes, field(pattern, "notes"));
    appendCondition(content, TEXT.disciplines, field(pattern, "disciplines"));
    appendCondition(content, TEXT.useWhen, field(pattern, "allowed_when"));
    appendCondition(content, TEXT.avoidWhen, field(pattern, "avoid_when"));

    article.append(meta, content);
    return article;
  }

  function syncQueryString() {
    const url = new URL(window.location.href);
    const query = elements.query.value.trim();
    if (query) url.searchParams.set("q", query);
    else url.searchParams.delete("q");
    window.history.replaceState(null, "", url);
  }

  function render() {
    const query = elements.query.value.trim();
    state.matches = state.patterns
      .filter(matchesFilters)
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

    if (!state.matches.length) {
      const empty = create("div", "empty-state");
      empty.append(create("h3", "", TEXT.emptyTitle), create("p", "", TEXT.emptyText));
      elements.results.append(empty);
      elements.status.textContent = TEXT.zero;
      elements.showMore.hidden = true;
      syncQueryString();
      return;
    }

    const shown = state.matches.slice(0, state.visibleLimit);
    for (const item of shown) elements.results.append(renderResult(item.pattern));
    elements.status.textContent = TEXT.count(state.matches.length, shown.length);
    elements.showMore.hidden = shown.length >= state.matches.length;
    syncQueryString();
  }

  function resetExplorer() {
    elements.form.reset();
    state.visibleLimit = 20;
    render();
    elements.query.focus();
  }

  async function loadPatterns() {
    try {
      const catalogUrl = new URL(explorer.dataset.catalogUrl, document.baseURI);
      const response = await fetch(catalogUrl, { cache: "no-cache" });
      if (!response.ok) throw new Error("HTTP " + response.status);
      const payload = await response.json();
      const records = Array.isArray(payload) ? payload : payload.entries || payload.phrases || payload.patterns;
      if (!Array.isArray(records) || records.length === 0) throw new Error("No pattern records found");

      state.patterns = records.filter((record) => record && typeof record === "object");
      populateSelect(elements.stage, uniqueValues(["section", "stage"]));
      populateSelect(elements.functionName, uniqueValues(["function", "rhetorical_function"]));
      populateSelect(elements.strength, uniqueValues(["claim_strength"]));
      populateSelect(elements.evidence, uniqueValues(["evidence_requirement"]));
      populateSelect(elements.risk, uniqueValues(["risk"]));

      const query = new URLSearchParams(window.location.search).get("q");
      if (query) elements.query.value = query;
      render();
    } catch (error) {
      elements.results.setAttribute("aria-busy", "false");
      const box = create("div", "error-state");
      box.append(create("h3", "", TEXT.unavailableTitle), create("p", "", TEXT.unavailableText));
      elements.results.replaceChildren(box);
      elements.status.textContent = TEXT.unavailableTitle;
      elements.showMore.hidden = true;
    }
  }

  elements.form.addEventListener("submit", (event) => {
    event.preventDefault();
    state.visibleLimit = 20;
    render();
  });

  elements.clear.addEventListener("click", resetExplorer);

  for (const select of [
    elements.stage,
    elements.functionName,
    elements.strength,
    elements.evidence,
    elements.risk,
  ]) {
    select.addEventListener("change", () => {
      state.visibleLimit = 20;
      render();
    });
  }

  let queryTimer;
  elements.query.addEventListener("input", () => {
    window.clearTimeout(queryTimer);
    queryTimer = window.setTimeout(() => {
      state.visibleLimit = 20;
      render();
    }, 140);
  });

  elements.showMore.addEventListener("click", () => {
    state.visibleLimit += 20;
    render();
  });

  loadPatterns();
}
