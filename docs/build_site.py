#!/usr/bin/env python3
"""Build the dependency-free bilingual RhetoriLex documentation site."""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import sys
from pathlib import Path
from typing import Any


DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent
BASE_URL = "https://rezaprama.github.io/RhetoriLex"
AUTHOR = "Reza Prama Arviandi"
OG_IMAGE = f"{BASE_URL}/assets/rhetorilex-hero.png"
WRITING_SKILLS_SOURCE = ROOT / "data" / "editorial" / "writing-skills.v1.json"
WRITING_SKILLS_ID = ROOT / "data" / "translations" / "writing-skills.id.v1.json"

ROUTES: dict[str, dict[str, str]] = {
    "home": {"en": "", "id": ""},
    "academic_writing": {"en": "academic-writing", "id": "penulisan-akademik"},
    "scientific_writing": {"en": "scientific-writing", "id": "penulisan-ilmiah"},
    "phrase_explorer": {"en": "phrase-explorer", "id": "penjelajah-frasa"},
    "paraphrasing": {"en": "paraphrasing", "id": "parafrasa"},
    "rhetorical_moves": {"en": "rhetorical-moves", "id": "gerakan-retoris"},
    "research_writing_guides": {
        "en": "research-writing-guides",
        "id": "panduan-penulisan-riset",
    },
    "agent_skills": {"en": "agent-skills", "id": "skill-agen"},
    "about": {"en": "about", "id": "tentang"},
    "research_gap": {"en": "research-gap", "id": "kesenjangan-riset"},
    "literature_review": {"en": "literature-review", "id": "tinjauan-pustaka"},
    "thesis": {"en": "thesis", "id": "tesis"},
    "methods": {"en": "methods", "id": "metode"},
    "results": {"en": "results", "id": "hasil"},
    "discussion": {"en": "discussion", "id": "diskusi"},
    "hedging": {"en": "hedging", "id": "hedging-akademik"},
    "reviewer_response": {"en": "reviewer-response", "id": "tanggapan-reviewer"},
    "association_vs_causation": {
        "en": "association-vs-causation",
        "id": "asosiasi-vs-kausalitas",
    },
    "preserve_claim_strength": {
        "en": "preserve-claim-strength",
        "id": "pertahankan-kekuatan-klaim",
    },
    "skills_research_framing": {
        "en": "writing-skills/research-framing",
        "id": "skill-penulisan/perumusan-riset",
    },
    "skills_literature_writing": {
        "en": "writing-skills/literature-writing",
        "id": "skill-penulisan/penulisan-literatur",
    },
    "skills_argumentation": {
        "en": "writing-skills/argumentation",
        "id": "skill-penulisan/argumentasi",
    },
    "skills_thesis_dissertation": {
        "en": "writing-skills/thesis-and-dissertation",
        "id": "skill-penulisan/tesis-dan-disertasi",
    },
    "skills_publication_writing": {
        "en": "writing-skills/publication-writing",
        "id": "skill-penulisan/penulisan-publikasi",
    },
    "skills_scientific_study_framing": {
        "en": "writing-skills/scientific-study-framing",
        "id": "skill-penulisan/perumusan-studi-ilmiah",
    },
    "skills_methods_writing": {
        "en": "writing-skills/methods-writing",
        "id": "skill-penulisan/penulisan-metode",
    },
    "skills_results_writing": {
        "en": "writing-skills/results-writing",
        "id": "skill-penulisan/penulisan-hasil",
    },
    "skills_discussion_writing": {
        "en": "writing-skills/discussion-writing",
        "id": "skill-penulisan/penulisan-diskusi",
    },
    "skills_scientific_claim_control": {
        "en": "writing-skills/scientific-claim-control",
        "id": "skill-penulisan/kontrol-klaim-ilmiah",
    },
    "skills_paraphrasing": {
        "en": "writing-skills/paraphrasing",
        "id": "skill-penulisan/parafrasa",
    },
}

LABELS: dict[str, dict[str, str]] = {
    "academic_writing": {"en": "Academic Writing", "id": "Penulisan Akademik"},
    "scientific_writing": {"en": "Scientific Writing", "id": "Penulisan Ilmiah"},
    "phrase_explorer": {"en": "Phrase Explorer", "id": "Penjelajah Frasa"},
    "paraphrasing": {"en": "Paraphrasing", "id": "Parafrasa"},
    "rhetorical_moves": {"en": "Rhetorical Moves", "id": "Gerakan Retoris"},
    "research_writing_guides": {
        "en": "Research Writing Guides",
        "id": "Panduan Penulisan Riset",
    },
    "agent_skills": {"en": "Agent Skills", "id": "Skill Agen"},
    "about": {"en": "About", "id": "Tentang"},
    "research_gap": {"en": "Research Gap", "id": "Kesenjangan Riset"},
    "literature_review": {"en": "Literature Review", "id": "Tinjauan Pustaka"},
    "thesis": {"en": "Thesis Writing", "id": "Penulisan Tesis"},
    "methods": {"en": "Methods Writing", "id": "Penulisan Metode"},
    "results": {"en": "Results Writing", "id": "Penulisan Hasil"},
    "discussion": {"en": "Discussion Writing", "id": "Penulisan Diskusi"},
    "hedging": {"en": "Academic Hedging", "id": "Hedging Akademik"},
    "reviewer_response": {"en": "Reviewer Response", "id": "Tanggapan Reviewer"},
    "association_vs_causation": {
        "en": "Association vs Causation",
        "id": "Asosiasi vs Kausalitas",
    },
    "preserve_claim_strength": {
        "en": "Preserve Claim Strength",
        "id": "Pertahankan Kekuatan Klaim",
    },
    "skills_research_framing": {"en": "Research Framing Skills", "id": "Skill Perumusan Riset"},
    "skills_literature_writing": {"en": "Literature Writing Skills", "id": "Skill Penulisan Literatur"},
    "skills_argumentation": {"en": "Argumentation Skills", "id": "Skill Argumentasi"},
    "skills_thesis_dissertation": {"en": "Thesis and Dissertation Skills", "id": "Skill Tesis dan Disertasi"},
    "skills_publication_writing": {"en": "Publication Writing Skills", "id": "Skill Penulisan Publikasi"},
    "skills_scientific_study_framing": {"en": "Scientific Study Framing Skills", "id": "Skill Perumusan Studi Ilmiah"},
    "skills_methods_writing": {"en": "Methods Writing Skills", "id": "Skill Penulisan Metode"},
    "skills_results_writing": {"en": "Results Writing Skills", "id": "Skill Penulisan Hasil"},
    "skills_discussion_writing": {"en": "Discussion Writing Skills", "id": "Skill Penulisan Diskusi"},
    "skills_scientific_claim_control": {"en": "Scientific Claim Control Skills", "id": "Skill Kontrol Klaim Ilmiah"},
    "skills_paraphrasing": {"en": "Paraphrasing Skills", "id": "Skill Parafrasa"},
}

CORE_KEYS = (
    "academic_writing",
    "scientific_writing",
    "phrase_explorer",
    "paraphrasing",
    "rhetorical_moves",
    "research_writing_guides",
    "agent_skills",
    "about",
)

UI: dict[str, dict[str, str]] = {
    "en": {
        "skip": "Skip to content",
        "primary": "Primary navigation",
        "index": "Index",
        "theme": "Theme",
        "system": "System",
        "light": "Light",
        "dark": "Dark",
        "switch": "Bahasa Indonesia",
        "switch_short": "ID",
        "home": "Home",
        "repository": "Repository",
        "provenance": "Provenance",
        "security": "Security",
        "license": "Licensing",
        "created": "Created by Reza Prama Arviandi.",
        "rights": "Editorial data: CC BY 4.0. Code: Apache 2.0.",
        "resources": "Project resources",
        "sections": "Writing index",
        "footer_note": "Original rhetorical patterns for evidence-calibrated academic writing.",
    },
    "id": {
        "skip": "Lewati ke isi",
        "primary": "Navigasi utama",
        "index": "Indeks",
        "theme": "Tema",
        "system": "Sistem",
        "light": "Terang",
        "dark": "Gelap",
        "switch": "English",
        "switch_short": "EN",
        "home": "Beranda",
        "repository": "Repositori",
        "provenance": "Provenans",
        "security": "Keamanan",
        "license": "Lisensi",
        "created": "Dibuat oleh Reza Prama Arviandi.",
        "rights": "Data editorial: CC BY 4.0. Kode: Apache 2.0.",
        "resources": "Sumber proyek",
        "sections": "Indeks penulisan",
        "footer_note": "Pola retoris orisinal untuk penulisan akademik yang selaras dengan bukti.",
    },
}

from site_content_en_primary import PAGES_EN as PAGES_EN_PRIMARY
from site_content_en_secondary import PAGES_EN as PAGES_EN_SECONDARY
from site_content_en_intents import PAGES_EN as PAGES_EN_INTENTS
from site_content_id_primary import PAGES_ID as PAGES_ID_PRIMARY
from site_content_id_secondary import PAGES_ID as PAGES_ID_SECONDARY
from site_content_id_intents import PAGES_ID as PAGES_ID_INTENTS
from site_content_skill_groups import GROUP_PAGES


PAGES: dict[str, dict[str, dict[str, str]]] = {
    key: {
        "en": PAGES_EN_PRIMARY.get(
            key,
            PAGES_EN_SECONDARY.get(key, PAGES_EN_INTENTS.get(key, GROUP_PAGES.get(key, {}).get("en", {}))),
        ),
        "id": PAGES_ID_PRIMARY.get(
            key,
            PAGES_ID_SECONDARY.get(key, PAGES_ID_INTENTS.get(key, GROUP_PAGES.get(key, {}).get("id", {}))),
        ),
    }
    for key in ROUTES
}


THEME_BOOTSTRAP = """<script>
(function () {
  var preference = "system";
  try {
    var saved = window.localStorage.getItem("rhetorilex.theme");
    if (saved === "light" || saved === "dark" || saved === "system") preference = saved;
  } catch (error) {}
  var dark = preference === "dark" ||
    (preference === "system" && window.matchMedia("(prefers-color-scheme: dark)").matches);
  document.documentElement.dataset.theme = dark ? "dark" : "light";
  document.documentElement.dataset.themePreference = preference;
}());
</script>"""


def route_path(locale: str, key: str) -> str:
    slug = ROUTES[key][locale]
    return f"{locale}/{slug}".rstrip("/")


def canonical_url(locale: str, key: str) -> str:
    return f"{BASE_URL}/{route_path(locale, key)}/"


def relative_href(locale: str, current_key: str, target_key: str, target_locale: str | None = None) -> str:
    destination_locale = target_locale or locale
    current_dir = route_path(locale, current_key)
    target_dir = route_path(destination_locale, target_key)
    relative = posixpath.relpath(target_dir, current_dir)
    return "./" if relative == "." else f"{relative}/"


def relative_asset(locale: str, current_key: str, asset: str) -> str:
    return posixpath.relpath(asset, route_path(locale, current_key))


def resolve_links(source: str, locale: str, current_key: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return relative_href(locale, current_key, match.group(1))

    return re.sub(r"\{\{link:([a-z_]+)\}\}", replace, source)


def nav_link(locale: str, current_key: str, target_key: str, class_name: str = "") -> str:
    current = ' aria-current="page"' if current_key == target_key else ""
    css = f' class="{class_name}"' if class_name else ""
    return (
        f'<a{css} href="{relative_href(locale, current_key, target_key)}"{current}>'
        f"{html.escape(LABELS[target_key][locale])}</a>"
    )


def render_header(locale: str, current_key: str) -> str:
    text = UI[locale]
    other_locale = "id" if locale == "en" else "en"
    primary_keys = (
        "academic_writing",
        "scientific_writing",
        "phrase_explorer",
        "research_writing_guides",
    )
    primary = "".join(nav_link(locale, current_key, key) for key in primary_keys)
    full_index = "".join(nav_link(locale, current_key, key) for key in CORE_KEYS)
    return f"""
<a class="skip-link" href="#main">{html.escape(text["skip"])}</a>
<header class="site-header">
  <div class="header-inner">
    <a class="wordmark" href="{relative_href(locale, current_key, "home")}" aria-label="RhetoriLex {html.escape(text["home"])}">RhetoriLex</a>
    <nav class="primary-nav" aria-label="{html.escape(text["primary"])}">{primary}</nav>
    <details class="index-menu">
      <summary>{html.escape(text["index"])}</summary>
      <nav class="index-panel" aria-label="{html.escape(text["sections"])}">{full_index}</nav>
    </details>
    <div class="site-tools">
      <a class="locale-switch" href="{relative_href(locale, current_key, current_key, other_locale)}" hreflang="{other_locale}" lang="{other_locale}" data-locale-link="{other_locale}" title="{html.escape(text["switch"])}">{html.escape(text["switch_short"])}</a>
      <label class="theme-picker">
        <span class="sr-only">{html.escape(text["theme"])}</span>
        <select data-theme-control aria-label="{html.escape(text["theme"])}">
          <option value="system">{html.escape(text["system"])}</option>
          <option value="light">{html.escape(text["light"])}</option>
          <option value="dark">{html.escape(text["dark"])}</option>
        </select>
      </label>
    </div>
  </div>
</header>"""


def render_footer(locale: str, current_key: str) -> str:
    text = UI[locale]
    creator_prefix = "Created by" if locale == "en" else "Dibuat oleh"
    writing_links = "".join(f"<li>{nav_link(locale, current_key, key)}</li>" for key in CORE_KEYS)
    return f"""
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-intro">
      <a class="wordmark" href="{relative_href(locale, current_key, "home")}">RhetoriLex</a>
      <p>{html.escape(text["footer_note"])}</p>
      <p>{creator_prefix} <a href="https://rezaprama.com" target="_blank" rel="noopener noreferrer">{AUTHOR}</a>.</p>
      <p>{html.escape(text["rights"])}</p>
    </div>
    <nav aria-label="{html.escape(text["sections"])}">
      <h2>{html.escape(text["sections"])}</h2>
      <ul>{writing_links}</ul>
    </nav>
    <nav aria-label="{html.escape(text["resources"])}">
      <h2>{html.escape(text["resources"])}</h2>
      <ul>
        <li><a href="https://github.com/rezaprama/RhetoriLex">{html.escape(text["repository"])}</a></li>
        <li><a href="https://github.com/rezaprama/RhetoriLex/blob/main/PROVENANCE.md">{html.escape(text["provenance"])}</a></li>
        <li><a href="https://github.com/rezaprama/RhetoriLex/blob/main/SECURITY.md">{html.escape(text["security"])}</a></li>
        <li><a href="https://github.com/rezaprama/RhetoriLex/blob/main/LICENSE">{html.escape(text["license"])}</a></li>
      </ul>
    </nav>
  </div>
</footer>"""


_WRITING_SKILL_CACHE: tuple[dict[str, Any], dict[str, dict[str, Any]]] | None = None


def load_writing_skills() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    global _WRITING_SKILL_CACHE
    if _WRITING_SKILL_CACHE is not None:
        return _WRITING_SKILL_CACHE
    source = json.loads(WRITING_SKILLS_SOURCE.read_text(encoding="utf-8"))
    translation = json.loads(WRITING_SKILLS_ID.read_text(encoding="utf-8"))
    raw_translations = translation.get("skills", translation.get("translations", {}))
    if isinstance(raw_translations, list):
        translations = {item["id"]: item for item in raw_translations}
    else:
        translations = dict(raw_translations)
    skills = source.get("skills", [])
    if source.get("count") != len(skills) or len(skills) != 144:
        raise ValueError("Writing-skill catalog must contain exactly 144 records")
    _WRITING_SKILL_CACHE = source, translations
    return _WRITING_SKILL_CACHE


def group_skills(group_id: str) -> list[dict[str, Any]]:
    source, _ = load_writing_skills()
    return [skill for skill in source["skills"] if skill.get("group") == group_id]


def group_route_key(group_id: str) -> str:
    for key, localized in GROUP_PAGES.items():
        if localized["en"]["group_id"] == group_id:
            return key
    raise KeyError(group_id)


def translated_skill(skill: dict[str, Any], locale: str) -> dict[str, Any]:
    if locale == "en":
        return skill
    _, translations = load_writing_skills()
    translated = translations.get(skill["id"], {})
    merged = dict(skill)
    merged["name"] = translated.get("name", skill.get("name", ""))
    merged["description"] = translated.get("description", skill.get("description", ""))
    return merged


def skill_url(locale: str, current_key: str, skill: dict[str, Any]) -> str:
    target_key = group_route_key(skill["group"])
    return f"{relative_href(locale, current_key, target_key)}#{skill['slug']}"


def structured_data(locale: str, key: str, page: dict[str, str]) -> dict[str, Any]:
    url = canonical_url(locale, key)
    person = {"@type": "Person", "name": AUTHOR, "url": "https://rezaprama.com"}
    if key == "home":
        entity: dict[str, Any] = {
            "@type": "WebSite",
            "@id": f"{url}#website",
            "url": url,
            "name": "RhetoriLex",
            "description": page["description"],
            "inLanguage": locale,
            "creator": person,
            "potentialAction": {
                "@type": "SearchAction",
                "target": {
                    "@type": "EntryPoint",
                    "urlTemplate": f"{canonical_url(locale, 'phrase_explorer')}?q={{search_term_string}}",
                },
                "query-input": "required name=search_term_string",
            },
        }
        return {"@context": "https://schema.org", "@graph": [entity]}

    page_type = "CollectionPage" if page["kind"] in {"explorer", "skill_group"} else "Article"
    entity = {
        "@type": page_type,
        "@id": f"{url}#page",
        "url": url,
        "name": page["h1"],
        "headline": page["h1"],
        "description": page["description"],
        "inLanguage": locale,
        "isAccessibleForFree": True,
        "author": person,
        "isPartOf": {"@type": "WebSite", "name": "RhetoriLex", "url": canonical_url(locale, "home")},
    }
    if key == "phrase_explorer":
        entity["mainEntity"] = {
            "@type": "Dataset",
            "name": "RhetoriLex rhetorical pattern catalog",
            "description": "Original academic English patterns with rhetorical and evidence metadata.",
            "url": f"{BASE_URL}/data/phrases.json",
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "creator": person,
            "inLanguage": "en",
            "distribution": {
                "@type": "DataDownload",
                "encodingFormat": "application/json",
                "contentUrl": f"{BASE_URL}/data/phrases.json",
            },
        }
    elif page["kind"] == "skill_group":
        items = group_skills(page["group_id"])
        entity["mainEntity"] = {
            "@type": "ItemList",
            "numberOfItems": len(items),
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": position,
                    "name": translated_skill(skill, locale).get("name", skill["id"]),
                    "url": f"{url}#{skill['slug']}",
                }
                for position, skill in enumerate(items, start=1)
            ],
        }
    breadcrumb = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": UI[locale]["home"],
                "item": canonical_url(locale, "home"),
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": LABELS[key][locale],
                "item": url,
            },
        ],
    }
    return {"@context": "https://schema.org", "@graph": [entity, breadcrumb]}


def render_head(locale: str, key: str, page: dict[str, str]) -> str:
    other_locale = "id" if locale == "en" else "en"
    og_locale = "en_US" if locale == "en" else "id_ID"
    og_alternate = "id_ID" if locale == "en" else "en_US"
    og_alt = (
        "RhetoriLex academic writing reference"
        if locale == "en"
        else "Referensi penulisan akademik RhetoriLex"
    )
    schema = json.dumps(structured_data(locale, key, page), ensure_ascii=False, separators=(",", ":"))
    title = html.escape(page["title"])
    description = html.escape(page["description"], quote=True)
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{THEME_BOOTSTRAP}
<meta name="description" content="{description}">
<meta name="author" content="{AUTHOR}">
<meta name="theme-color" content="#f5f3ed" data-theme-color>
<link rel="canonical" href="{canonical_url(locale, key)}">
<link rel="alternate" hreflang="en" href="{canonical_url("en", key)}">
<link rel="alternate" hreflang="id" href="{canonical_url("id", key)}">
<link rel="alternate" hreflang="x-default" href="{canonical_url("en", key)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="RhetoriLex">
<meta property="og:locale" content="{og_locale}">
<meta property="og:locale:alternate" content="{og_alternate}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical_url(locale, key)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:alt" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{OG_IMAGE}">
<title>{title}</title>
<link rel="icon" href="{relative_asset(locale, key, "assets/icon.svg")}" type="image/svg+xml">
<link rel="manifest" href="{relative_asset(locale, key, "site.webmanifest")}">
<link rel="stylesheet" href="{relative_asset(locale, key, "styles.css")}">
<script type="application/ld+json">{schema}</script>
<script src="{relative_asset(locale, key, "app.js")}" defer></script>"""


def render_breadcrumb(locale: str, key: str) -> str:
    return f"""<nav class="breadcrumb" aria-label="Breadcrumb">
  <ol>
    <li><a href="{relative_href(locale, key, "home")}">{html.escape(UI[locale]["home"])}</a></li>
    <li aria-current="page">{html.escape(LABELS[key][locale])}</li>
  </ol>
</nav>"""


def render_home_main(locale: str, page: dict[str, str]) -> str:
    if locale == "en":
        label = "Describe your rhetorical intent"
        placeholder = "e.g. compare results without implying causation"
        button = "Search phrases"
        note = "Interface language and pattern language are separate. Phrase patterns remain in English."
        secondary = "Explore writing skills"
        github = "View on GitHub"
    else:
        label = "Jelaskan tujuan retoris Anda"
        placeholder = "contoh: bandingkan hasil tanpa menyiratkan sebab"
        button = "Cari frasa"
        note = "Bahasa antarmuka dan bahasa pola dipisahkan. Pola frasa tetap dalam bahasa Inggris."
        secondary = "Jelajahi skill penulisan"
        github = "Lihat di GitHub"
    body = resolve_links(page["body"], locale, "home")
    return f"""
<main id="main">
  <section class="home-intro">
    <div class="home-intro-inner">
      <h1>{html.escape(page["h1"])}</h1>
      <p class="lede">{html.escape(page["lede"])}</p>
      <form class="intent-search" action="{relative_href(locale, "home", "phrase_explorer")}" method="get" role="search">
        <label for="home-query">{html.escape(label)}</label>
        <div class="search-row">
          <input id="home-query" name="q" type="search" placeholder="{html.escape(placeholder, quote=True)}" autocomplete="off">
          <button class="primary-button" type="submit">{html.escape(button)}</button>
        </div>
      </form>
      <p class="pattern-language">{html.escape(note)}</p>
      <div class="home-links">
        <a href="{relative_href(locale, "home", "skills_research_framing")}">{html.escape(secondary)}</a>
        <a href="https://github.com/rezaprama/RhetoriLex" target="_blank" rel="noopener noreferrer">{html.escape(github)}</a>
      </div>
    </div>
  </section>
  <div class="page-frame home-content">{body}</div>
</main>"""


def explorer_labels(locale: str) -> dict[str, str]:
    if locale == "en":
        return {
            "search_label": "Rhetorical intent",
            "placeholder": "e.g. cautious interpretation of an observational result",
            "search": "Search",
            "filters": "Refine by metadata",
            "stage": "Manuscript stage",
            "function": "Rhetorical function",
            "strength": "Claim strength",
            "evidence": "Evidence requirement",
            "risk": "Risk",
            "all_stage": "All stages",
            "all_function": "All functions",
            "all_strength": "Any strength",
            "all_evidence": "Any evidence requirement",
            "all_risk": "Any risk level",
            "clear": "Clear",
            "loading": "Loading the local reference catalog...",
            "noscript": "JavaScript is required for interactive search. The static guide and local command-line interface remain available.",
            "more": "Show more results",
        }
    return {
        "search_label": "Tujuan retoris",
        "placeholder": "contoh: interpretasi hati-hati untuk hasil observasional",
        "search": "Cari",
        "filters": "Saring berdasarkan metadata",
        "stage": "Tahap naskah",
        "function": "Fungsi retoris",
        "strength": "Kekuatan klaim",
        "evidence": "Kebutuhan bukti",
        "risk": "Risiko",
        "all_stage": "Semua tahap",
        "all_function": "Semua fungsi",
        "all_strength": "Semua kekuatan",
        "all_evidence": "Semua kebutuhan bukti",
        "all_risk": "Semua tingkat risiko",
        "clear": "Bersihkan",
        "loading": "Memuat katalog referensi lokal...",
        "noscript": "JavaScript diperlukan untuk pencarian interaktif. Panduan statis dan antarmuka baris perintah lokal tetap tersedia.",
        "more": "Tampilkan hasil lainnya",
    }


def render_explorer_main(locale: str, key: str, page: dict[str, str]) -> str:
    labels = explorer_labels(locale)
    body = resolve_links(page["body"], locale, key)
    catalog_url = relative_asset(locale, key, "data/phrases.json")
    return f"""
<main id="main" class="article-page">
  <div class="page-frame">
    {render_breadcrumb(locale, key)}
    <header class="article-header">
      <h1>{html.escape(page["h1"])}</h1>
      <p class="lede">{html.escape(page["lede"])}</p>
    </header>
    <section class="explorer-workspace" data-explorer data-locale="{locale}" data-catalog-url="{catalog_url}" aria-labelledby="explorer-form-title">
      <h2 class="sr-only" id="explorer-form-title">{html.escape(LABELS[key][locale])}</h2>
      <form class="explorer-form" id="explorer-form" role="search">
        <label class="explorer-query" for="query">
          <span>{html.escape(labels["search_label"])}</span>
          <input id="query" name="q" type="search" placeholder="{html.escape(labels["placeholder"], quote=True)}" autocomplete="off">
        </label>
        <div class="explorer-actions">
          <button class="primary-button" type="submit">{html.escape(labels["search"])}</button>
          <button class="secondary-button" id="clear-search" type="button">{html.escape(labels["clear"])}</button>
        </div>
        <details class="filter-panel">
          <summary>{html.escape(labels["filters"])}</summary>
          <div class="filter-grid">
            <label for="section-filter"><span>{html.escape(labels["stage"])}</span><select id="section-filter" name="stage"><option value="">{html.escape(labels["all_stage"])}</option></select></label>
            <label for="function-filter"><span>{html.escape(labels["function"])}</span><select id="function-filter" name="function"><option value="">{html.escape(labels["all_function"])}</option></select></label>
            <label for="strength-filter"><span>{html.escape(labels["strength"])}</span><select id="strength-filter" name="strength"><option value="">{html.escape(labels["all_strength"])}</option></select></label>
            <label for="evidence-filter"><span>{html.escape(labels["evidence"])}</span><select id="evidence-filter" name="evidence"><option value="">{html.escape(labels["all_evidence"])}</option></select></label>
            <label for="risk-filter"><span>{html.escape(labels["risk"])}</span><select id="risk-filter" name="risk"><option value="">{html.escape(labels["all_risk"])}</option></select></label>
          </div>
        </details>
      </form>
      <div class="explorer-status" id="explorer-status" role="status" aria-live="polite">{html.escape(labels["loading"])}</div>
      <div class="results" id="results" aria-live="polite" aria-busy="true"></div>
      <button class="secondary-button show-more" id="show-more" type="button" hidden>{html.escape(labels["more"])}</button>
      <div class="copy-status" id="copy-status" role="status" aria-live="polite"></div>
      <noscript><p class="notice">{html.escape(labels["noscript"])}</p></noscript>
    </section>
    <div class="article-body explorer-guide">{body}</div>
  </div>
</main>"""


def render_skill_group_main(locale: str, key: str, page: dict[str, str]) -> str:
    skills = group_skills(page["group_id"])
    source, _ = load_writing_skills()
    by_id = {skill["id"]: skill for skill in source["skills"]}
    if locale == "en":
        count_label = f"{len(skills)} writing skills"
        index_label = "On this page"
        objective_label = "Rhetorical objective"
        uses_label = "Use cases"
        example_label = "Original example"
        functions_label = "Related phrase functions"
        related_label = "Related skills"
        warning_label = "Evidence and claim warning"
        copy_label = "Copy example"
        permalink_label = "Permanent link"
        language_notice = ""
    else:
        count_label = f"{len(skills)} skill penulisan"
        index_label = "Dalam halaman ini"
        objective_label = "Tujuan retoris"
        uses_label = "Kegunaan"
        example_label = "Contoh orisinal"
        functions_label = "Fungsi frasa terkait"
        related_label = "Skill terkait"
        warning_label = "Peringatan bukti dan klaim"
        copy_label = "Salin contoh"
        permalink_label = "Tautan tetap"
        language_notice = (
            '<p class="pattern-language">Nama dan definisi tersedia dalam Bahasa Indonesia. '
            'Contoh pola, tujuan teknis, dan peringatan tetap dalam bahasa Inggris untuk menjaga '
            'kontrak canonical.</p>'
        )

    index_items: list[str] = []
    entries: list[str] = []
    for skill in skills:
        expected_canonical = f"/en/writing-skills/{page['group_id']}/#{skill['slug']}"
        if skill.get("canonical_en") != expected_canonical:
            raise ValueError(f"Invalid canonical_en for {skill['id']}")
        localized = translated_skill(skill, locale)
        name = html.escape(str(localized.get("name", skill["id"])))
        description = html.escape(str(localized.get("description", "")))
        slug = html.escape(str(skill["slug"]), quote=True)
        skill_id = html.escape(str(skill["id"]))
        index_items.append(f'<li><a href="#{slug}">{name}</a></li>')

        objective = html.escape(str(skill.get("rhetorical_objective", "")))
        raw_uses = skill.get("use_cases", [])
        uses = raw_uses if isinstance(raw_uses, list) else [raw_uses]
        use_items = "".join(f"<li>{html.escape(str(item))}</li>" for item in uses if item)
        example = str(skill.get("example", ""))
        example_escaped = html.escape(example)
        example_attr = html.escape(example, quote=True)
        raw_functions = skill.get("related_phrase_functions", [])
        functions = raw_functions if isinstance(raw_functions, list) else [raw_functions]
        function_text = ", ".join(html.escape(str(item)) for item in functions if item)
        related_links: list[str] = []
        for related_id in skill.get("related_skill_ids", []):
            target = by_id.get(related_id)
            if target:
                target_name = translated_skill(target, locale).get("name", related_id)
                related_links.append(
                    f'<a href="{skill_url(locale, key, target)}">{html.escape(str(target_name))}</a>'
                )
        warning = html.escape(str(skill.get("evidence_claim_warning", "")))
        language = ' lang="en"' if locale == "id" else ""
        details = [
            f'<div><dt>{objective_label}</dt><dd{language}>{objective}</dd></div>' if objective else "",
            (
                f'<div><dt>{uses_label}</dt><dd{language}><ul>{use_items}</ul></dd></div>'
                if use_items
                else ""
            ),
            (
                f'<div><dt>{functions_label}</dt><dd{language}>{function_text}</dd></div>'
                if function_text
                else ""
            ),
            (
                f'<div><dt>{related_label}</dt><dd>{", ".join(related_links)}</dd></div>'
                if related_links
                else ""
            ),
            f'<div><dt>{warning_label}</dt><dd{language}>{warning}</dd></div>' if warning else "",
        ]
        example_block = ""
        if example:
            example_block = (
                f'<div class="skill-example"><h3>{example_label}</h3>'
                f'<p class="phrase-template"{language}>{example_escaped}</p>'
                f'<button class="copy-button" type="button" data-copy-value="{example_attr}">{copy_label}</button></div>'
            )
        entries.append(
            f"""<article class="skill-reference" id="{slug}">
  <header class="skill-reference-header">
    <div><code>{skill_id}</code><span>{html.escape(str(skill.get("domain", "")))}</span></div>
    <h2>{name}</h2>
    <a href="#{slug}">{permalink_label}</a>
  </header>
  <div class="skill-reference-body">
    <p class="entry-description">{description}</p>
    {example_block}
    <dl class="skill-facts">{''.join(details)}</dl>
  </div>
</article>"""
        )

    body = resolve_links(page["body"], locale, key)
    return f"""
<main id="main" class="article-page">
  <div class="page-frame">
    {render_breadcrumb(locale, key)}
    <header class="article-header skill-group-header">
      <h1>{html.escape(page["h1"])}</h1>
      <p class="lede">{html.escape(page["lede"])}</p>
      <p class="catalog-count">{html.escape(count_label)}</p>
      {language_notice}
    </header>
    <nav class="skill-page-index" aria-label="{html.escape(index_label)}">
      <h2>{html.escape(index_label)}</h2>
      <ol>{''.join(index_items)}</ol>
    </nav>
    <div class="skill-catalog">{''.join(entries)}</div>
    <div class="copy-status" id="copy-status" role="status" aria-live="polite"></div>
    <div class="article-body skill-group-guide">{body}</div>
  </div>
</main>"""


def render_article_main(locale: str, key: str, page: dict[str, str]) -> str:
    body = resolve_links(page["body"], locale, key)
    return f"""
<main id="main" class="article-page">
  <div class="page-frame">
    {render_breadcrumb(locale, key)}
    <article>
      <header class="article-header">
        <h1>{html.escape(page["h1"])}</h1>
        <p class="lede">{html.escape(page["lede"])}</p>
      </header>
      <div class="article-body">{body}</div>
    </article>
  </div>
</main>"""


def render_page(locale: str, key: str) -> str:
    page = PAGES[key][locale]
    if not page:
        raise ValueError(f"Missing {locale} content for {key}")
    if page["kind"] == "home":
        main = render_home_main(locale, page)
    elif page["kind"] == "explorer":
        main = render_explorer_main(locale, key, page)
    elif page["kind"] == "skill_group":
        main = render_skill_group_main(locale, key, page)
    else:
        main = render_article_main(locale, key, page)
    return f"""<!doctype html>
<html lang="{locale}" data-locale="{locale}">
<head>
{render_head(locale, key, page)}
</head>
<body>
{render_header(locale, key)}
{main}
{render_footer(locale, key)}
</body>
</html>
"""


def render_root() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{THEME_BOOTSTRAP}
<meta name="robots" content="noindex,follow">
<meta name="description" content="Choose English or Bahasa Indonesia for the RhetoriLex academic writing index.">
<meta name="theme-color" content="#f5f3ed" data-theme-color>
<link rel="canonical" href="{BASE_URL}/">
<link rel="alternate" hreflang="en" href="{canonical_url("en", "home")}">
<link rel="alternate" hreflang="id" href="{canonical_url("id", "home")}">
<link rel="alternate" hreflang="x-default" href="{BASE_URL}/">
<meta http-equiv="refresh" content="8;url=./en/">
<title>Choose Language | RhetoriLex</title>
<link rel="icon" href="assets/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="styles.css">
<script>
(function () {{
  var locale = "";
  try {{
    var saved = window.localStorage.getItem("rhetorilex.locale");
    if (saved === "en" || saved === "id") locale = saved;
  }} catch (error) {{}}
  if (!locale) locale = navigator.language && navigator.language.toLowerCase().indexOf("id") === 0 ? "id" : "en";
  window.location.replace("./" + locale + "/");
}}());
</script>
</head>
<body class="locale-root">
<main id="main" class="locale-chooser">
  <p class="wordmark">RhetoriLex</p>
  <h1>Choose a language <span lang="id">Pilih bahasa</span></h1>
  <p>Open the scholarly writing index in English or Bahasa Indonesia.</p>
  <nav aria-label="Language">
    <a class="primary-button" href="./en/" hreflang="en" lang="en">English</a>
    <a class="secondary-button" href="./id/" hreflang="id" lang="id">Bahasa Indonesia</a>
  </nav>
  <noscript><p>Automatic language selection is unavailable. Choose a link above.</p></noscript>
</main>
</body>
</html>
"""


def render_sitemap() -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for key in ROUTES:
        for locale in ("en", "id"):
            lines.extend(
                [
                    "  <url>",
                    f"    <loc>{canonical_url(locale, key)}</loc>",
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{canonical_url("en", key)}" />',
                    f'    <xhtml:link rel="alternate" hreflang="id" href="{canonical_url("id", key)}" />',
                    f'    <xhtml:link rel="alternate" hreflang="x-default" href="{canonical_url("en", key)}" />',
                    "  </url>",
                ]
            )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def generated_files() -> dict[Path, str]:
    files: dict[Path, str] = {DOCS / "index.html": render_root()}
    for key in ROUTES:
        for locale in ("en", "id"):
            files[DOCS / route_path(locale, key) / "index.html"] = render_page(locale, key)
    files[DOCS / "sitemap.xml"] = render_sitemap()
    files[DOCS / "robots.txt"] = (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {BASE_URL}/sitemap.xml\n"
    )
    manifest = {
        "name": "RhetoriLex Academic Writing Index",
        "short_name": "RhetoriLex",
        "description": "Original rhetorical patterns for evidence-calibrated academic writing.",
        "start_url": "./en/",
        "scope": "./",
        "display": "standalone",
        "background_color": "#f5f3ed",
        "theme_color": "#164f7a",
        "icons": [
            {
                "src": "assets/icon.svg",
                "sizes": "any",
                "type": "image/svg+xml",
                "purpose": "any",
            }
        ],
    }
    files[DOCS / "site.webmanifest"] = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    return files


def build(check: bool) -> int:
    outdated: list[str] = []
    for path, content in generated_files().items():
        if check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                outdated.append(path.relative_to(DOCS).as_posix())
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    if outdated:
        print("Generated site is out of date:")
        for path in outdated:
            print(f"  {path}")
        return 1
    if check:
        print("Generated site is current.")
    else:
        print(f"Wrote {len(generated_files())} deterministic site files.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify generated files without writing.")
    args = parser.parse_args()
    return build(args.check)


if __name__ == "__main__":
    sys.exit(main())
