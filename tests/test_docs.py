from __future__ import annotations

from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


class DocumentationTests(unittest.TestCase):
    def test_local_markdown_links_resolve(self) -> None:
        missing: list[str] = []
        documents = sorted(ROOT.glob("*.md")) + sorted((ROOT / "docs").rglob("*.md"))
        for document in documents:
            text = document.read_text(encoding="utf-8")
            for raw in LINK_RE.findall(text):
                target = raw.strip().split(maxsplit=1)[0].strip("<>'\"")
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or target.startswith(("#", "mailto:")):
                    continue
                relative = unquote(parsed.path)
                if not relative:
                    continue
                resolved = (document.parent / relative).resolve()
                try:
                    resolved.relative_to(ROOT.resolve())
                except ValueError:
                    missing.append(f"{document.relative_to(ROOT)}: escapes repository: {target}")
                    continue
                if not resolved.exists():
                    missing.append(f"{document.relative_to(ROOT)}: {target}")
        self.assertEqual(missing, [])

    def test_no_draft_markers_in_public_docs(self) -> None:
        failures: list[str] = []
        for document in sorted(ROOT.glob("*.md")) + sorted((ROOT / "docs").rglob("*.md")):
            text = document.read_text(encoding="utf-8")
            if re.search(r"\b(?:TODO|TBD|FIXME)\b", text):
                failures.append(str(document.relative_to(ROOT)))
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
