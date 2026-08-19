from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rhetorilex.cli import main  # noqa: E402


class CliTests(unittest.TestCase):
    def capture(self, arguments: list[str]) -> tuple[int, str]:
        output = io.StringIO()
        with redirect_stdout(output):
            code = main(arguments)
        return code, output.getvalue()

    def test_search_json(self) -> None:
        code, output = self.capture(["--json", "search", "causal effect", "--limit", "2"])
        self.assertEqual(code, 0)
        self.assertEqual(len(json.loads(output)), 2)

    def test_explain(self) -> None:
        code, output = self.capture(["explain", "RLX-POS-001"])
        self.assertEqual(code, 0)
        self.assertIn("Contract: valid", output)

    def test_inspect_validation(self) -> None:
        code, output = self.capture(["inspect", "--validate"])
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(output)["valid"])

    def test_taxonomy_and_random(self) -> None:
        code, taxonomy = self.capture(["taxonomy", "claim_strengths"])
        self.assertEqual(code, 0)
        self.assertEqual(len(json.loads(taxonomy)), 4)
        code, first = self.capture(["random", "--seed", "repeat", "--function", "define_scope"])
        self.assertEqual(code, 0)
        code, second = self.capture(["random", "--seed", "repeat", "--function", "define_scope"])
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
