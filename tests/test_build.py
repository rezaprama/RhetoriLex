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
                "dist/SHA256SUMS",
                "dist/rhetorilex-v0.1.csv",
                "dist/rhetorilex-v0.1.json",
                "assets/patterns.json",
                "dist/phrases.json",
                "dist/rhetorilex-v0.1.md",
                "dist/rhetorilex-v0.1.sqlite3",
                "resources/catalog.json",
                "resources/evidence_claim_contract.json",
                "resources/phrases.json",
                "resources/taxonomy.json",
            }
            self.assertEqual(set(digest_tree(first)), expected)
            catalog = json.loads((first / "dist" / "rhetorilex-v0.1.json").read_text(encoding="utf-8"))
            self.assertEqual(catalog["entry_count"], 48)
            connection = sqlite3.connect(first / "dist" / "rhetorilex-v0.1.sqlite3")
            try:
                count = connection.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
            finally:
                connection.close()
            self.assertEqual(count, 48)


if __name__ == "__main__":
    unittest.main()
