from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SEARCH = ROOT / "skills" / "rhetorilex" / "scripts" / "search.py"
SKILL_ROOT = ROOT / "skills" / "rhetorilex"


class WritingSkillSearchTests(unittest.TestCase):
    def run_search(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SEARCH), *arguments],
            cwd=SKILL_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_exact_name_and_slug_retrieve_same_skill(self) -> None:
        by_name = self.run_search(
            "Association vs causation",
            "--writing-skills",
            "--json",
            "--limit",
            "1",
        )
        by_slug = self.run_search(
            "--skill-slug",
            "association-vs-causation",
            "--json",
        )
        self.assertEqual(by_name.returncode, 0, by_name.stderr)
        self.assertEqual(by_slug.returncode, 0, by_slug.stderr)
        name_row = json.loads(by_name.stdout)[0]
        slug_row = json.loads(by_slug.stdout)[0]
        self.assertEqual(name_row["id"], slug_row["id"])
        self.assertEqual(slug_row["group"], "scientific-claim-control")
        self.assertIn("distinguish_causation", slug_row["related_phrase_functions"])

    def test_group_browse_returns_exact_methods_inventory(self) -> None:
        result = self.run_search(
            "--writing-skills",
            "--skill-group",
            "methods-writing",
            "--json",
            "--limit",
            "50",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        self.assertEqual(len(rows), 19)
        self.assertTrue(all(row["group"] == "methods-writing" for row in rows))

    def test_indonesian_mode_localises_interface_not_english_example(self) -> None:
        result = self.run_search(
            "--skill-slug",
            "citation-preserving-rewrite",
            "--language",
            "id",
            "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        row = json.loads(result.stdout)[0]
        self.assertEqual(
            row["localized_interface"]["name"],
            "Penulisan ulang dengan sitasi tetap",
        )
        self.assertTrue(row["example"].startswith("Source:"))
        self.assertNotIn("example", row["localized_interface"])

    def test_group_discovery_lists_eleven_substantive_routes(self) -> None:
        result = self.run_search("--list-writing-skill-groups")
        self.assertEqual(result.returncode, 0, result.stderr)
        groups = json.loads(result.stdout)
        self.assertEqual(len(groups), 11)
        self.assertEqual(sum(group["count"] for group in groups), 144)
        self.assertTrue(
            all(group["canonical_en"].startswith("/en/writing-skills/") for group in groups)
        )

    def test_unknown_group_fails_with_discovery_hint(self) -> None:
        result = self.run_search(
            "--writing-skills",
            "--skill-group",
            "not-a-group",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown --skill-group", result.stderr)


if __name__ == "__main__":
    unittest.main()

