from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CONFIG = DOCS / "content" / "copy-lint.json"


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.suppressed = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "template"}:
            self.suppressed += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "template"}:
            self.suppressed = max(0, self.suppressed - 1)

    def handle_data(self, data: str) -> None:
        if not self.suppressed:
            self.parts.append(data)

    @property
    def text(self) -> str:
        return " ".join(" ".join(self.parts).split())


def visible_html(path: Path) -> str:
    parser = VisibleTextParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.text


class SiteCopyLintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads(CONFIG.read_text(encoding="utf-8"))

    def test_allowlist_contract_is_explicit(self) -> None:
        contract = self.config["allowlist_contract"]
        self.assertEqual(set(contract["required_fields"]), {"path", "phrase", "reason"})
        self.assertTrue(contract["rule"])
        forbidden = {phrase.casefold() for phrase in self.config["forbidden_phrases"]}
        for entry in self.config["technical_context_allowlist"]:
            self.assertEqual({"path", "phrase", "reason"} - entry.keys(), set())
            self.assertIn(entry["phrase"].casefold(), forbidden)
            self.assertTrue(entry["path"])
            self.assertTrue(entry["reason"])

    def test_visible_site_and_readme_copy_has_no_unreviewed_filler(self) -> None:
        allowlist = {
            (entry["path"].replace("\\", "/"), entry["phrase"].casefold())
            for entry in self.config["technical_context_allowlist"]
        }
        sources: dict[str, str] = {}
        for path in DOCS.rglob("*.html"):
            sources[path.relative_to(ROOT).as_posix()] = visible_html(path)
        for name in ("README.md", "README.id.md"):
            path = ROOT / name
            sources[name] = path.read_text(encoding="utf-8")

        violations: list[str] = []
        for relative, text in sources.items():
            folded = text.casefold()
            for phrase in self.config["forbidden_phrases"]:
                if phrase.casefold() in folded and (relative, phrase.casefold()) not in allowlist:
                    violations.append(f"{relative}: {phrase}")
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
