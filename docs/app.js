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

const APP_SCRIPT_URL = document.currentScript && document.currentScript.src ? document.currentScript.src : "";
if ("serviceWorker" in navigator && APP_SCRIPT_URL) {
  const serviceWorkerUrl = new URL("service-worker.js", APP_SCRIPT_URL);
  navigator.serviceWorker.register(serviceWorkerUrl).catch(() => {});
}

const REMOTE_CALL_LIMIT = 3;
const workbench = document.querySelector("[data-paraphrase-workbench]");

if (workbench) {
  const locale = workbench.dataset.locale === "id" ? "id" : "en";
  const STORAGE = {
    endpoint: "rhetorilex.workbench.endpoint",
    model: "rhetorilex.workbench.model",
    token: "rhetorilex.workbench.token",
    save: "rhetorilex.workbench.save",
    usage: "rhetorilex.workbench.usage",
  };

  const TEXT = {
    en: {
      empty: "Paste text before building a prompt.",
      promptReady: "Prompt ready. No endpoint call was made.",
      endpointMissing: "Endpoint is empty. Prompt-only output is ready below.",
      calling: "Calling endpoint. Review output before use.",
      done: "Rewrite returned. Check protected meaning before submission.",
      failed: "Endpoint call failed. Prompt remains available for manual use.",
      limit: (remaining) => remaining + " of " + REMOTE_CALL_LIMIT + " endpoint calls remain today in this browser.",
      limitReached: "Daily browser limit reached. Prompt-only mode still works.",
      protectedFallback: "Claim strength and evidence scope",
      found: "visible",
      check: "check manually",
      rewritePlaceholder: "No rewrite yet.",
      promptTitle: "Use this prompt with your own trusted model.",
      noEndpoint: "No endpoint call. Copy the prompt to a trusted local or provider model.",
    },
    id: {
      empty: "Tempel teks sebelum membuat prompt.",
      promptReady: "Prompt siap. Tidak ada panggilan endpoint.",
      endpointMissing: "Endpoint kosong. Output prompt saja tersedia di bawah.",
      calling: "Memanggil endpoint. Tinjau output sebelum dipakai.",
      done: "Parafrasa diterima. Cek makna terlindungi sebelum dikumpulkan.",
      failed: "Panggilan endpoint gagal. Prompt tetap tersedia untuk penggunaan manual.",
      limit: (remaining) => remaining + " dari " + REMOTE_CALL_LIMIT + " panggilan endpoint tersisa hari ini di browser ini.",
      limitReached: "Batas harian browser tercapai. Mode prompt saja tetap bekerja.",
      protectedFallback: "Kekuatan klaim dan cakupan bukti",
      found: "terlihat",
      check: "cek manual",
      rewritePlaceholder: "Belum ada parafrasa.",
      promptTitle: "Gunakan prompt ini dengan model tepercaya milik Anda.",
      noEndpoint: "Tidak ada panggilan endpoint. Salin prompt ke model lokal atau provider tepercaya.",
    },
  }[locale];

  const elements = {
    form: document.querySelector("#paraphrase-form"),
    source: document.querySelector("#paraphrase-source"),
    mode: document.querySelector("#paraphrase-mode"),
    target: document.querySelector("#paraphrase-target"),
    protected: document.querySelector("#paraphrase-protected"),
    endpoint: document.querySelector("#paraphrase-endpoint"),
    model: document.querySelector("#paraphrase-model"),
    token: document.querySelector("#paraphrase-token"),
    save: document.querySelector("#paraphrase-save"),
    draft: document.querySelector("#paraphrase-draft"),
    clear: document.querySelector("#paraphrase-clear"),
    limit: document.querySelector("#paraphrase-limit"),
    status: document.querySelector("#paraphrase-status"),
    invariants: document.querySelector("#paraphrase-invariants"),
    prompt: document.querySelector("#paraphrase-prompt"),
    output: document.querySelector("#paraphrase-output"),
  };

  function todayKey() {
    const now = new Date();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    return now.getFullYear() + "-" + month + "-" + day;
  }

  function usageState() {
    const empty = { day: todayKey(), count: 0 };
    try {
      const saved = JSON.parse(window.localStorage.getItem(STORAGE.usage) || "null");
      if (!saved || saved.day !== empty.day || typeof saved.count !== "number") return empty;
      return saved;
    } catch (error) {
      return empty;
    }
  }

  function remainingCalls() {
    return Math.max(0, REMOTE_CALL_LIMIT - usageState().count);
  }

  function incrementCalls() {
    const current = usageState();
    current.count += 1;
    writePreference(STORAGE.usage, JSON.stringify(current));
    updateLimitText();
  }

  function updateLimitText() {
    if (elements.limit) elements.limit.textContent = TEXT.limit(remainingCalls());
  }

  function createNode(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function splitExtra(value) {
    return value
      .split(/[\n;,]+/)
      .map((item) => item.trim())
      .filter(Boolean);
  }

  function addMatches(set, text, pattern) {
    for (const match of text.matchAll(pattern)) {
      const value = match[0].trim();
      if (value) set.add(value);
    }
  }

  function extractInvariants(source, extra) {
    const values = new Set(splitExtra(extra));
    addMatches(values, source, /\([A-Z][^()]{0,90}\d{4}[a-z]?[^()]*\)/g);
    addMatches(values, source, /\[[0-9,\s-]+\]/g);
    addMatches(values, source, /\b\d+(?:[.,]\d+)?(?:\s?(?:%|percent|weeks?|months?|years?|days?|kg|g|mg|ml|cm|mm|m|n|p|CI|OR|RR|HR))?\b/gi);
    addMatches(values, source, /\b(no|not|without|never|cannot|only|within|under|may|might|could|suggests?|associated with|correlated with|predicts?|causes?|caused|led to|increased|decreased|reduced)\b/gi);
    if (!values.size) values.add(TEXT.protectedFallback);
    return [...values].slice(0, 40);
  }

  function modeInstruction(mode) {
    if (mode === "plain") return "Rewrite in clear technical prose for a broad academic reader. Preserve technical terms when a synonym would change meaning.";
    if (mode === "concise") return "Make the passage more concise. Remove redundancy, but do not remove evidence, conditions, citations, or uncertainty.";
    if (mode === "idfriendly") return "Rewrite in natural academic English that remains friendly to Indonesian writers. Avoid idioms, ornate phrasing, and unnecessary nominalisations.";
    return "Rewrite in academic prose while preserving the exact claim, evidence boundary, uncertainty, citation support, and causal status.";
  }

  function buildPrompt(source, invariants) {
    const target = elements.target.value.trim();
    const protectedTerms = invariants.map((item) => "- " + item).join("\n");
    const parts = [
      "Role: RhetoriLex, a meaning-preserving paraphrase assistant for academic and technical writing.",
      "Task: " + modeInstruction(elements.mode.value),
      "Protected meaning. Do not change or omit these unless the user explicitly says so:\n" + protectedTerms,
      target ? "User target note:\n" + target : "",
      "Rules:\n- Do not fabricate citations, data, methods, mechanisms, or novelty.\n- Do not turn association into causation or weak evidence into strong claims.\n- Preserve citations, numbers, units, negation, direction, scope, population, time, and uncertainty.\n- If a protected element cannot be retained naturally, flag it instead of deleting it.",
      "Return format:\n1. Rewrite\n2. Protected-meaning checklist\n3. Remaining risks or manual checks",
      "Source text:\n" + source,
    ];
    return parts.filter(Boolean).join("\n\n");
  }

  function renderInvariants(items, output) {
    const outputText = (output || "").toLocaleLowerCase();
    const nodes = items.map((item) => {
      const li = createNode("li");
      li.append(createNode("span", "audit-item", item));
      if (output) {
        const visible = outputText.includes(item.toLocaleLowerCase());
        li.append(createNode("span", visible ? "audit-tag" : "audit-tag audit-tag-check", visible ? TEXT.found : TEXT.check));
      }
      return li;
    });
    elements.invariants.replaceChildren(...nodes);
  }

  function saveSettings() {
    if (elements.save.checked) {
      writePreference(STORAGE.save, "1");
      writePreference(STORAGE.endpoint, elements.endpoint.value.trim());
      writePreference(STORAGE.model, elements.model.value.trim());
      writePreference(STORAGE.token, elements.token.value.trim());
      return;
    }
    try {
      window.localStorage.removeItem(STORAGE.save);
      window.localStorage.removeItem(STORAGE.endpoint);
      window.localStorage.removeItem(STORAGE.model);
      window.localStorage.removeItem(STORAGE.token);
    } catch (error) {
      return;
    }
  }

  function loadSettings() {
    const shouldSave = readPreference(STORAGE.save) === "1";
    elements.save.checked = shouldSave;
    if (!shouldSave) return;
    elements.endpoint.value = readPreference(STORAGE.endpoint) || "";
    elements.model.value = readPreference(STORAGE.model) || "";
    elements.token.value = readPreference(STORAGE.token) || "";
  }

  function extractModelText(payload) {
    if (!payload || typeof payload !== "object") return "";
    if (typeof payload.output_text === "string") return payload.output_text;
    const choices = Array.isArray(payload.choices) ? payload.choices : [];
    if (choices[0] && choices[0].message && typeof choices[0].message.content === "string") {
      return choices[0].message.content;
    }
    const output = Array.isArray(payload.output) ? payload.output : [];
    for (const item of output) {
      const content = Array.isArray(item.content) ? item.content : [];
      const text = content.map((part) => part.text || part.output_text || "").join("\n").trim();
      if (text) return text;
    }
    const candidates = Array.isArray(payload.candidates) ? payload.candidates : [];
    const parts = candidates[0] && candidates[0].content ? candidates[0].content.parts || [] : [];
    return parts.map((part) => part.text || "").join("\n").trim();
  }

  function isGeminiNative(endpoint) {
    return endpoint.includes("generativelanguage.googleapis.com") && !endpoint.includes("/openai/");
  }

  function requestBody(endpoint, prompt) {
    if (isGeminiNative(endpoint)) {
      return {
        contents: [{ role: "user", parts: [{ text: prompt }] }],
        generationConfig: { temperature: 0.2 },
      };
    }
    return {
      model: elements.model.value.trim() || "local-model",
      messages: [
        { role: "system", content: "You are RhetoriLex. Rewrite safely without adding evidence, citations, or stronger claims." },
        { role: "user", content: prompt },
      ],
      temperature: 0.2,
    };
  }

  function requestHeaders(endpoint, token) {
    const headers = { "Content-Type": "application/json" };
    if (!token) return headers;
    if (isGeminiNative(endpoint)) headers["x-goog-api-key"] = token;
    else headers.Authorization = "Bearer " + token;
    return headers;
  }

  async function callEndpoint(endpoint, prompt) {
    const token = elements.token.value.trim();
    const response = await fetch(endpoint, {
      method: "POST",
      headers: requestHeaders(endpoint, token),
      body: JSON.stringify(requestBody(endpoint, prompt)),
    });
    if (!response.ok) throw new Error("HTTP " + response.status);
    const payload = await response.json();
    const text = extractModelText(payload);
    if (!text) throw new Error("Empty model response");
    return text;
  }

  function preparePromptOnly(statusText) {
    const source = elements.source.value.trim();
    if (!source) {
      elements.status.textContent = TEXT.empty;
      return null;
    }
    saveSettings();
    const invariants = extractInvariants(source, elements.protected.value);
    const prompt = buildPrompt(source, invariants);
    renderInvariants(invariants, "");
    elements.prompt.textContent = prompt;
    elements.output.textContent = TEXT.rewritePlaceholder;
    elements.status.textContent = statusText;
    return { source, invariants, prompt };
  }

  elements.draft.addEventListener("click", () => {
    preparePromptOnly(TEXT.promptReady);
  });

  elements.form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const prepared = preparePromptOnly(TEXT.promptTitle);
    if (!prepared) return;
    const endpoint = elements.endpoint.value.trim();
    if (!endpoint) {
      elements.status.textContent = TEXT.endpointMissing + " " + TEXT.noEndpoint;
      return;
    }
    if (remainingCalls() <= 0) {
      elements.status.textContent = TEXT.limitReached;
      return;
    }
    elements.status.textContent = TEXT.calling;
    try {
      const rewritten = await callEndpoint(endpoint, prepared.prompt);
      incrementCalls();
      elements.output.textContent = rewritten;
      renderInvariants(prepared.invariants, rewritten);
      elements.status.textContent = TEXT.done;
    } catch (error) {
      elements.status.textContent = TEXT.failed + " " + error.message;
    }
  });

  elements.clear.addEventListener("click", () => {
    elements.source.value = "";
    elements.target.value = "";
    elements.protected.value = "";
    elements.prompt.textContent = "";
    elements.output.textContent = TEXT.rewritePlaceholder;
    elements.invariants.replaceChildren();
    elements.status.textContent = TEXT.noEndpoint;
    elements.source.focus();
  });

  loadSettings();
  updateLimitText();
  elements.output.textContent = TEXT.rewritePlaceholder;
}
