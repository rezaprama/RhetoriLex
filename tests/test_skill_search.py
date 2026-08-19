from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SEARCH = ROOT / "skills" / "rhetorilex" / "scripts" / "search.py"
SKILL = ROOT / "skills" / "rhetorilex"


class SkillSearchTests(unittest.TestCase):
    def run_search(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SEARCH), *arguments],
            cwd=SKILL,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_alias_search_finds_integrity_pattern(self) -> None:
        result = self.run_search("ethical paraphrase preserve citation", "--json", "--limit", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        self.assertEqual(rows[0]["function"], "paraphrase_with_attribution")
        self.assertIn("paraphrasing", rows[0]["skill_areas"])

    def test_filter_only_section_browse(self) -> None:
        result = self.run_search(
            "--section",
            "peer_review_response",
            "--skill-area",
            "reviewer_response",
            "--json",
            "--limit",
            "10",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(row["function"] == "respond_reviewer" for row in rows))

    def test_taxonomy_discovery_lists_facets(self) -> None:
        result = self.run_search("--list-skill-areas")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 13)
        result = self.run_search("--list-domains")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 10)

    def test_search_is_offline_stdlib_only(self) -> None:
        source = SEARCH.read_text(encoding="utf-8")
        for dependency in ("requests", "numpy", "pandas", "scipy"):
            self.assertNotIn(f"import {dependency}", source)


if __name__ == "__main__":
    unittest.main()
