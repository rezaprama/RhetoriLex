from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        for name in ("href", "src"):
            if values.get(name):
                self.references.append(values[name] or "")


class StaticSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = (DOCS / "index.html").read_text(encoding="utf-8")
        cls.parser = PageParser()
        cls.parser.feed(cls.html)

    def test_required_explorer_controls_exist(self) -> None:
        required = {
            "explorer-form",
            "query",
            "section-filter",
            "function-filter",
            "strength-filter",
            "explorer-status",
            "results",
        }
        self.assertEqual(required - self.parser.ids, set())

    def test_local_html_references_exist(self) -> None:
        missing: list[str] = []
        for reference in self.parser.references:
            parsed = urlsplit(reference)
            if parsed.scheme or parsed.netloc or reference.startswith(("#", "mailto:")):
                continue
            relative = unquote(parsed.path).lstrip("/")
            if relative and not (DOCS / relative).is_file():
                missing.append(reference)
        self.assertEqual(missing, [])

    def test_visible_page_avoids_em_dash_and_placeholders(self) -> None:
        self.assertNotIn("—", self.html)
        self.assertNotIn("TODO", self.html)
        self.assertNotIn("example.com", self.html)

    def test_explorer_data_contract(self) -> None:
        payload = json.loads((ROOT / "data" / "dist" / "phrases.json").read_text(encoding="utf-8"))
        entries = payload["entries"]
        self.assertEqual(len(entries), 48)
        required = {
            "id",
            "function",
            "template",
            "stage",
            "claim_strength",
            "evidence_requirement",
            "risk",
            "provenance",
        }
        for entry in entries:
            self.assertEqual(required - entry.keys(), set(), entry.get("id"))

    def test_explorer_uses_safe_dom_and_stage_fallback(self) -> None:
        script = (DOCS / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("innerHTML", script)
        self.assertIn('field(pattern, "section", "stage")', script)
        self.assertIn('normalizedField(pattern, "evidence_requirement")', script)
        self.assertIn('field(pattern, "causal_design_required") === true', script)
        self.assertIn("CAUTION_INTENT_TERMS", script)
        self.assertIn("textContent", script)


if __name__ == "__main__":
    unittest.main()
