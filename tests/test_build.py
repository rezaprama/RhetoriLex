from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def digest_tree(path: Path) -> dict[str, str]:
    return {
        item.relative_to(path).as_posix(): hashlib.sha256(item.read_bytes()).hexdigest()
        for item in sorted(path.rglob("*"))
        if item.is_file()
    }


class BuildTests(unittest.TestCase):
    def test_build_is_deterministic_and_complete(self) -> None:
        with tempfile.TemporaryDirectory() as first_raw, tempfile.TemporaryDirectory() as second_raw:
            first = Path(first_raw)
            second = Path(second_raw)
            for target in (first, second):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "scripts" / "build_data.py"),
                        "--dist",
                        str(target / "dist"),
                        "--resources",
                        str(target / "resources"),
                        "--skill-assets",
                        str(target / "assets"),
                    ],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(digest_tree(first), digest_tree(second))
            expected = {
                "assets/patterns.json",
                "assets/search-aliases.json",
                "assets/taxonomy.json",
                "assets/writing-skills.json",
                "assets/writing-skills.id.json",
                "dist/SHA256SUMS",
                "dist/phrases.json",
                "dist/writing-skills.json",
                "dist/writing-skills.id.json",
                "dist/rhetorilex-v0.2.csv",
                "dist/rhetorilex-v0.2.json",
                "dist/rhetorilex-v0.2.md",
                "dist/rhetorilex-v0.2.sqlite3",
                "resources/canonical_manifest.json",
                "resources/catalog.json",
                "resources/evidence_claim_contract.json",
                "resources/phrases.json",
                "resources/search_aliases.json",
                "resources/taxonomy.json",
                "resources/writing_skills.json",
                "resources/writing_skills_id.json",
            }
            self.assertEqual(set(digest_tree(first)), expected)
            catalog = json.loads(
                (first / "dist" / "rhetorilex-v0.2.json").read_text(encoding="utf-8")
            )
            self.assertEqual(catalog["release_version"], "0.2.0")
            self.assertEqual(catalog["format_version"], "2.0.0")
            self.assertEqual(catalog["taxonomy_version"], "1.1.0")
            self.assertEqual(catalog["entry_count"], 96)
            self.assertTrue(all(row["domains"] for row in catalog["entries"]))
            self.assertTrue(all(row["skill_areas"] for row in catalog["entries"]))
            self.assertTrue(all(row["search_aliases"] for row in catalog["entries"]))
            writing_skills = json.loads(
                (first / "dist" / "writing-skills.json").read_text(encoding="utf-8")
            )
            writing_skills_id = json.loads(
                (first / "dist" / "writing-skills.id.json").read_text(encoding="utf-8")
            )
            self.assertEqual(writing_skills["count"], 144)
            self.assertEqual(writing_skills["group_count"], 11)
            self.assertEqual(
                [row["id"] for row in writing_skills_id["skills"]],
                [row["id"] for row in writing_skills["skills"]],
            )

            connection = sqlite3.connect(first / "dist" / "rhetorilex-v0.2.sqlite3")
            try:
                count = connection.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
                columns = {
                    row[1] for row in connection.execute("PRAGMA table_info(entries)").fetchall()
                }
            finally:
                connection.close()
            self.assertEqual(count, 96)
            self.assertTrue(
                {"domains_json", "skill_areas_json", "search_aliases_json"} <= columns
            )

    def test_workspace_build_has_no_stale_v01_release(self) -> None:
        stale = sorted((ROOT / "data" / "dist").glob("rhetorilex-v0.1.*"))
        self.assertEqual(stale, [])


if __name__ == "__main__":
    unittest.main()