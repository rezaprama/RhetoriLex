from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASE_URL = "https://rezaprama.github.io/RhetoriLex"

ROUTE_PAIRS = [
    ("", ""),
    ("academic-writing", "penulisan-akademik"),
    ("scientific-writing", "penulisan-ilmiah"),
    ("phrase-explorer", "penjelajah-frasa"),
    ("paraphrasing", "parafrasa"),
    ("paraphrase-workbench", "alat-parafrasa"),
    ("rhetorical-moves", "gerakan-retoris"),
    ("research-writing-guides", "panduan-penulisan-riset"),
    ("agent-skills", "skill-agen"),
    ("about", "tentang"),
    ("research-gap", "kesenjangan-riset"),
    ("literature-review", "tinjauan-pustaka"),
    ("thesis", "tesis"),
    ("methods", "metode"),
    ("results", "hasil"),
    ("discussion", "diskusi"),
    ("hedging", "hedging-akademik"),
    ("reviewer-response", "tanggapan-reviewer"),
    ("association-vs-causation", "asosiasi-vs-kausalitas"),
    ("preserve-claim-strength", "pertahankan-kekuatan-klaim"),
    ("writing-skills/research-framing", "skill-penulisan/perumusan-riset"),
    ("writing-skills/literature-writing", "skill-penulisan/penulisan-literatur"),
    ("writing-skills/argumentation", "skill-penulisan/argumentasi"),
    ("writing-skills/thesis-and-dissertation", "skill-penulisan/tesis-dan-disertasi"),
    ("writing-skills/publication-writing", "skill-penulisan/penulisan-publikasi"),
    ("writing-skills/scientific-study-framing", "skill-penulisan/perumusan-studi-ilmiah"),
    ("writing-skills/methods-writing", "skill-penulisan/penulisan-metode"),
    ("writing-skills/results-writing", "skill-penulisan/penulisan-hasil"),
    ("writing-skills/discussion-writing", "skill-penulisan/penulisan-diskusi"),
    ("writing-skills/scientific-claim-control", "skill-penulisan/kontrol-klaim-ilmiah"),
    ("writing-skills/paraphrasing", "skill-penulisan/parafrasa"),
]

GROUP_COUNTS = {
    "research-framing": 11,
    "literature-writing": 13,
    "argumentation": 15,
    "thesis-and-dissertation": 13,
    "publication-writing": 12,
    "scientific-study-framing": 6,
    "methods-writing": 19,
    "results-writing": 17,
    "discussion-writing": 13,
    "scientific-claim-control": 11,
    "paraphrasing": 14,
}

GROUP_ROUTE_PAIRS = {
    "research-framing": ("writing-skills/research-framing", "skill-penulisan/perumusan-riset"),
    "literature-writing": ("writing-skills/literature-writing", "skill-penulisan/penulisan-literatur"),
    "argumentation": ("writing-skills/argumentation", "skill-penulisan/argumentasi"),
    "thesis-and-dissertation": (
        "writing-skills/thesis-and-dissertation",
        "skill-penulisan/tesis-dan-disertasi",
    ),
    "publication-writing": ("writing-skills/publication-writing", "skill-penulisan/penulisan-publikasi"),
    "scientific-study-framing": (
        "writing-skills/scientific-study-framing",
        "skill-penulisan/perumusan-studi-ilmiah",
    ),
    "methods-writing": ("writing-skills/methods-writing", "skill-penulisan/penulisan-metode"),
    "results-writing": ("writing-skills/results-writing", "skill-penulisan/penulisan-hasil"),
    "discussion-writing": ("writing-skills/discussion-writing", "skill-penulisan/penulisan-diskusi"),
    "scientific-claim-control": (
        "writing-skills/scientific-claim-control",
        "skill-penulisan/kontrol-klaim-ilmiah",
    ),
    "paraphrasing": ("writing-skills/paraphrasing", "skill-penulisan/parafrasa"),
}


def route_file(locale: str, slug: str) -> Path:
    return DOCS / locale / slug / "index.html" if slug else DOCS / locale / "index.html"


def route_url(locale: str, slug: str) -> str:
    suffix = f"/{slug}" if slug else ""
    return f"{BASE_URL}/{locale}{suffix}/"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.references: list[str] = []
        self.title_parts: list[str] = []
        self.h1_parts: list[str] = []
        self.visible_parts: list[str] = []
        self.main_parts: list[str] = []
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self.alternates: dict[str, str] = {}
        self.schemas: list[str] = []
        self.lang = ""
        self._in_title = False
        self._in_h1 = False
        self._in_main = 0
        self._suppressed = 0
        self._schema_buffer: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang") or ""
        if values.get("id"):
            self.ids.add(values["id"] or "")
        for name in ("href", "src", "action"):
            if values.get(name):
                self.references.append(values[name] or "")
        if tag == "meta":
            key = values.get("name") or values.get("property") or values.get("http-equiv")
            if key:
                self.meta[key] = values.get("content") or ""
        if tag == "link":
            relations = set((values.get("rel") or "").split())
            if "canonical" in relations:
                self.canonical = values.get("href") or ""
            if "alternate" in relations and values.get("hreflang"):
                self.alternates[values["hreflang"] or ""] = values.get("href") or ""
        if tag == "title":
            self._in_title = True
        if tag == "h1":
            self._in_h1 = True
        if tag == "main":
            self._in_main += 1
        if tag in {"script", "style", "template"}:
            if tag == "script" and values.get("type") == "application/ld+json":
                self._schema_buffer = []
            self._suppressed += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if tag == "h1":
            self._in_h1 = False
        if tag == "main":
            self._in_main = max(0, self._in_main - 1)
        if tag in {"script", "style", "template"}:
            if tag == "script" and self._schema_buffer is not None:
                self.schemas.append("".join(self._schema_buffer))
                self._schema_buffer = None
            self._suppressed = max(0, self._suppressed - 1)

    def handle_data(self, data: str) -> None:
        if self._schema_buffer is not None:
            self._schema_buffer.append(data)
        if self._in_title:
            self.title_parts.append(data)
        if self._in_h1:
            self.h1_parts.append(data)
        if not self._suppressed:
            self.visible_parts.append(data)
            if self._in_main:
                self.main_parts.append(data)

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())

    @property
    def h1(self) -> str:
        return " ".join("".join(self.h1_parts).split())

    @property
    def visible_text(self) -> str:
        return " ".join(" ".join(self.visible_parts).split())

    @property
    def main_text(self) -> str:
        return " ".join(" ".join(self.main_parts).split())


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def local_target(page: Path, reference: str) -> tuple[Path | None, str]:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("mailto:", "tel:")):
        return None, parsed.fragment
    if parsed.path.startswith("/"):
        raise AssertionError(f"Root-domain path is not project-base safe: {page}: {reference}")
    raw_path = unquote(parsed.path)
    target = page if not raw_path else (page.parent / raw_path).resolve()
    if raw_path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target, parsed.fragment


class StaticSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.localized_pages: list[tuple[str, str, Path, PageParser]] = []
        for en_slug, id_slug in ROUTE_PAIRS:
            for locale, slug in (("en", en_slug), ("id", id_slug)):
                path = route_file(locale, slug)
                parser = parse_page(path)
                cls.localized_pages.append((locale, slug, path, parser))

    def test_generated_site_is_current(self) -> None:
        result = subprocess.run(
            [sys.executable, str(DOCS / "build_site.py"), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_required_localized_routes_exist_without_extras(self) -> None:
        expected = {
            route_file(locale, slug).resolve()
            for en_slug, id_slug in ROUTE_PAIRS
            for locale, slug in (("en", en_slug), ("id", id_slug))
        }
        actual = {
            path.resolve()
            for locale in ("en", "id")
            for path in (DOCS / locale).rglob("index.html")
        }
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 62)

    def test_homepage_h1_and_required_intents(self) -> None:
        en = parse_page(DOCS / "en" / "index.html")
        id_page = parse_page(DOCS / "id" / "index.html")
        self.assertEqual(
            en.h1,
            "Free local academic paraphrase skill for researchers.",
        )
        self.assertEqual(
            id_page.h1,
            "Skill parafrasa akademik lokal dan gratis.",
        )
        for phrase in ("Explore writing skills", "Search phrases", "View on GitHub"):
            self.assertIn(phrase, en.visible_text)
        for phrase in ("Popular writing tasks", "Browse by paper section", "Paraphrase Workbench", "Open dataset"):
            self.assertIn(phrase, en.visible_text)

    def test_unique_localized_metadata_and_complete_hreflang(self) -> None:
        titles: list[str] = []
        descriptions: list[str] = []
        h1s: list[str] = []
        for locale, slug, path, parser in self.localized_pages:
            with self.subTest(path=path):
                expected_url = route_url(locale, slug)
                counterpart_slug = next(
                    id_slug if locale == "en" else en_slug
                    for en_slug, id_slug in ROUTE_PAIRS
                    if slug == (en_slug if locale == "en" else id_slug)
                )
                self.assertEqual(parser.lang, locale)
                self.assertEqual(parser.canonical, expected_url)
                self.assertEqual(parser.alternates[locale], expected_url)
                self.assertEqual(parser.alternates["en"], route_url("en", slug if locale == "en" else counterpart_slug))
                self.assertEqual(parser.alternates["id"], route_url("id", counterpart_slug if locale == "en" else slug))
                self.assertEqual(parser.alternates["x-default"], parser.alternates["en"])
                self.assertTrue(parser.title)
                self.assertTrue(parser.meta.get("description"))
                self.assertEqual(parser.meta.get("og:url"), expected_url)
                self.assertEqual(parser.meta.get("twitter:card"), "summary_large_image")
                expected_alt = (
                    "RhetoriLex academic writing reference"
                    if locale == "en"
                    else "Referensi penulisan akademik RhetoriLex"
                )
                self.assertEqual(parser.meta.get("og:image:alt"), expected_alt)
                self.assertEqual(len(parser.schemas), 1)
                schema = json.loads(parser.schemas[0])
                self.assertEqual(schema["@context"], "https://schema.org")
                titles.append(parser.title)
                descriptions.append(parser.meta["description"])
                h1s.append(parser.h1)
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(len(descriptions), len(set(descriptions)))
        self.assertEqual(len(h1s), len(set(h1s)))

    def test_root_is_accessible_noindex_locale_chooser(self) -> None:
        html = (DOCS / "index.html").read_text(encoding="utf-8")
        parser = parse_page(DOCS / "index.html")
        self.assertEqual(parser.meta.get("robots"), "noindex,follow")
        self.assertEqual(parser.canonical, f"{BASE_URL}/")
        self.assertEqual(parser.alternates["en"], f"{BASE_URL}/en/")
        self.assertEqual(parser.alternates["id"], f"{BASE_URL}/id/")
        self.assertIn("./en/", parser.references)
        self.assertIn("./id/", parser.references)
        self.assertIn("rhetorilex.locale", html)
        self.assertIn("navigator.language", html)
        self.assertIn("<noscript>", html)

    def test_local_references_and_fragments_resolve(self) -> None:
        parser_cache: dict[Path, PageParser] = {}
        missing: list[str] = []
        for _, _, page, parser in self.localized_pages:
            for reference in parser.references:
                target, fragment = local_target(page, reference)
                if target is None:
                    continue
                if target == (DOCS / "data" / "phrases.json").resolve():
                    self.assertTrue((ROOT / "data" / "dist" / "phrases.json").is_file())
                    continue
                if not target.is_file():
                    missing.append(f"{page.relative_to(ROOT)} -> {reference}")
                    continue
                if fragment and target.suffix.lower() == ".html":
                    target_parser = parser_cache.setdefault(target, parse_page(target))
                    if fragment not in target_parser.ids:
                        missing.append(f"{page.relative_to(ROOT)} -> {reference} missing fragment")
        self.assertEqual(missing, [])

    def test_theme_bootstrap_precedes_css_and_has_three_persistent_modes(self) -> None:
        for _, _, path, _ in self.localized_pages:
            html_text = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertLess(
                    html_text.index("rhetorilex.theme"),
                    html_text.index('rel="stylesheet"'),
                )
                self.assertIn('value="system"', html_text)
                self.assertIn('value="light"', html_text)
                self.assertIn('value="dark"', html_text)
        script = (DOCS / "app.js").read_text(encoding="utf-8")
        self.assertIn("window.localStorage.setItem", script)
        self.assertIn("prefers-color-scheme: dark", script)
        self.assertIn("data-theme-control", script)

    def test_explorer_contract_is_project_base_safe_and_accessible(self) -> None:
        required_ids = {
            "explorer-form",
            "query",
            "section-filter",
            "function-filter",
            "strength-filter",
            "evidence-filter",
            "risk-filter",
            "explorer-status",
            "results",
            "show-more",
            "copy-status",
        }
        for path in (
            DOCS / "en" / "phrase-explorer" / "index.html",
            DOCS / "id" / "penjelajah-frasa" / "index.html",
        ):
            parser = parse_page(path)
            html_text = path.read_text(encoding="utf-8")
            self.assertEqual(required_ids - parser.ids, set())
            self.assertIn('data-catalog-url="../../data/phrases.json"', html_text)
            self.assertIn("<noscript>", html_text)
        script = (DOCS / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("innerHTML", script)
        self.assertIn("new URL(explorer.dataset.catalogUrl, document.baseURI)", script)
        self.assertIn("payload.entries || payload.phrases || payload.patterns", script)
        self.assertIn('field(pattern, "causal_design_required") === true', script)
        self.assertIn('field(pattern, "evidence_requirement")', script)
        self.assertIn('field(pattern, "risk")', script)
        self.assertIn("CAUTION_INTENT_TERMS", script)
        self.assertIn("QUERY_ALIASES", script)
        self.assertIn("textContent", script)
        self.assertNotIn('fetch("/data', script)

    def test_paraphrase_workbench_contract_is_installable_and_limited(self) -> None:
        required_ids = {
            "paraphrase-form",
            "paraphrase-source",
            "paraphrase-mode",
            "paraphrase-target",
            "paraphrase-protected",
            "paraphrase-endpoint",
            "paraphrase-model",
            "paraphrase-token",
            "paraphrase-save",
            "paraphrase-submit",
            "paraphrase-draft",
            "paraphrase-clear",
            "paraphrase-limit",
            "paraphrase-status",
            "paraphrase-invariants",
            "paraphrase-prompt",
            "paraphrase-output",
            "paraphrase-warning",
        }
        for path in (
            DOCS / "en" / "paraphrase-workbench" / "index.html",
            DOCS / "id" / "alat-parafrasa" / "index.html",
        ):
            parser = parse_page(path)
            html_text = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertEqual(required_ids - parser.ids, set())
                self.assertIn("data-paraphrase-workbench", html_text)
                self.assertIn("<noscript>", html_text)
                self.assertIn("3", parser.visible_text)

        script = (DOCS / "app.js").read_text(encoding="utf-8")
        self.assertIn("const REMOTE_CALL_LIMIT = 3", script)
        self.assertIn("rhetorilex.workbench.usage", script)
        self.assertIn("Authorization", script)
        self.assertIn("x-goog-api-key", script)
        self.assertIn("serviceWorker", script)
        self.assertIn("data-paraphrase-workbench", script)
        self.assertNotIn("innerHTML", script)

        manifest = json.loads((DOCS / "site.webmanifest").read_text(encoding="utf-8"))
        self.assertEqual(manifest["start_url"], "./en/paraphrase-workbench/")
        self.assertEqual(manifest["display"], "standalone")
        self.assertTrue((DOCS / "service-worker.js").is_file())

    def test_phrase_catalog_is_96_records_across_canonical_and_distributions(self) -> None:
        canonical_dir = ROOT / "data" / "canonical"
        manifest = json.loads(
            (canonical_dir / "catalog-manifest.v2.json").read_text(encoding="utf-8")
        )
        canonical = [
            json.loads(line)
            for shard in manifest["shards"]
            for line in (canonical_dir / shard).read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        dist_payload = json.loads((ROOT / "data" / "dist" / "phrases.json").read_text(encoding="utf-8"))
        bundled_payload = json.loads(
            (ROOT / "skills" / "rhetorilex" / "assets" / "patterns.json").read_text(encoding="utf-8")
        )
        dist = dist_payload["entries"]
        bundled = (
            bundled_payload
            if isinstance(bundled_payload, list)
            else bundled_payload.get("entries", bundled_payload.get("patterns", []))
        )
        self.assertEqual(manifest["entry_count"], 96)
        self.assertEqual(len(canonical), manifest["entry_count"])
        self.assertEqual(len(dist), 96)
        self.assertEqual(len(bundled), 96)
        self.assertEqual({item["id"] for item in canonical}, {item["id"] for item in dist})
        self.assertEqual({item["id"] for item in canonical}, {item["id"] for item in bundled})
        required = {
            "id",
            "function",
            "template",
            "stage",
            "claim_strength",
            "evidence_requirement",
            "causal_design_required",
            "risk",
            "notes",
            "provenance",
        }
        for entry in dist:
            self.assertEqual(required - entry.keys(), set(), entry.get("id"))
        self.assertEqual(
            {entry["evidence_requirement"] for entry in dist},
            {"none", "contextual", "observational", "direct", "convergent"},
        )

    def test_writing_skill_catalog_and_fragments(self) -> None:
        source = json.loads(
            (ROOT / "data" / "editorial" / "writing-skills.v1.json").read_text(encoding="utf-8")
        )
        translation = json.loads(
            (ROOT / "data" / "translations" / "writing-skills.id.v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(source["count"], 144)
        self.assertEqual(len(source["skills"]), 144)
        self.assertEqual({group["id"]: group["count"] for group in source["groups"]}, GROUP_COUNTS)
        self.assertEqual({item["id"] for item in translation["skills"]}, {item["id"] for item in source["skills"]})
        counts = Counter(item["group"] for item in source["skills"])
        self.assertEqual(dict(counts), GROUP_COUNTS)

        page_ids: dict[tuple[str, str], set[str]] = {}
        for group_id, (en_slug, id_slug) in GROUP_ROUTE_PAIRS.items():
            page_ids[("en", group_id)] = parse_page(route_file("en", en_slug)).ids
            page_ids[("id", group_id)] = parse_page(route_file("id", id_slug)).ids
        for skill in source["skills"]:
            expected = f"/en/writing-skills/{skill['group']}/#{skill['slug']}"
            self.assertEqual(skill["canonical_en"], expected)
            self.assertIn(skill["slug"], page_ids[("en", skill["group"])])
            self.assertIn(skill["slug"], page_ids[("id", skill["group"])])

    def test_i18n_glossary_is_complete_and_visible(self) -> None:
        glossary = json.loads((DOCS / "i18n" / "glossary.json").read_text(encoding="utf-8"))
        keys = [term["key"] for term in glossary["terms"]]
        self.assertEqual(len(keys), len(set(keys)))
        en_text = " ".join(parser.visible_text for locale, _, _, parser in self.localized_pages if locale == "en")
        id_text = " ".join(parser.visible_text for locale, _, _, parser in self.localized_pages if locale == "id")
        for term in glossary["terms"]:
            self.assertTrue(term["en"])
            self.assertTrue(term["id"])
            self.assertIn(term["en"], en_text, term["key"])
            self.assertIn(term["id"], id_text, term["key"])
        self.assertEqual(glossary["pattern_language"], "English")

    def test_pages_are_substantive_and_not_doorways(self) -> None:
        for locale, slug, path, parser in self.localized_pages:
            words = re.findall(r"\b[\w'-]+\b", parser.main_text)
            with self.subTest(locale=locale, slug=slug):
                self.assertGreaterEqual(len(words), 130, path)
                if slug:
                    self.assertGreaterEqual(parser.main_text.count("."), 3, path)

    def test_sitemap_has_absolute_urls_and_complete_alternates(self) -> None:
        root = ET.parse(DOCS / "sitemap.xml").getroot()
        ns = {
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xhtml": "http://www.w3.org/1999/xhtml",
        }
        expected = {
            route_url(locale, slug)
            for en_slug, id_slug in ROUTE_PAIRS
            for locale, slug in (("en", en_slug), ("id", id_slug))
        }
        urls = root.findall("sm:url", ns)
        actual = {item.findtext("sm:loc", namespaces=ns) for item in urls}
        self.assertEqual(actual, expected)
        self.assertNotIn(f"{BASE_URL}/", actual)
        for item in urls:
            links = item.findall("xhtml:link", ns)
            hreflangs = {link.attrib["hreflang"] for link in links}
            self.assertEqual(hreflangs, {"en", "id", "x-default"})
            for link in links:
                self.assertTrue(link.attrib["href"].startswith(f"{BASE_URL}/"))

    def test_no_external_runtime_or_forbidden_visual_tells(self) -> None:
        for _, _, path, parser in self.localized_pages:
            html_text = path.read_text(encoding="utf-8")
            self.assertNotIn("—", html_text)
            self.assertNotIn("–", html_text)
            for reference in parser.references:
                parsed = urlsplit(reference)
                if parsed.scheme in {"http", "https"}:
                    continue
                if reference.endswith((".css", ".js")):
                    target, _ = local_target(path, reference)
                    self.assertIsNotNone(target)
                    self.assertTrue(target.is_file())
        css = (DOCS / "styles.css").read_text(encoding="utf-8").lower()
        script = (DOCS / "app.js").read_text(encoding="utf-8")
        for forbidden in (
            "linear-gradient",
            "radial-gradient",
            "conic-gradient",
            "backdrop-filter",
            "box-shadow",
            "animation:",
            "transition:",
        ):
            self.assertNotIn(forbidden, css)
        self.assertNotIn("window.addEventListener(\"scroll\"", script)
        self.assertNotIn("—", script)
        self.assertNotIn("–", script)

    def test_creator_attribution_is_linked_safely(self) -> None:
        for locale, slug, path, _ in self.localized_pages:
            html_text = path.read_text(encoding="utf-8")
            with self.subTest(locale=locale, slug=slug):
                self.assertIn(
                    '<a href="https://rezaprama.com" target="_blank" rel="noopener noreferrer">'
                    "Reza Prama Arviandi</a>",
                    html_text,
                )


if __name__ == "__main__":
    unittest.main()
