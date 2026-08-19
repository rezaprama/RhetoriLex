from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rhetorilex import Catalog  # noqa: E402


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = Catalog.load()

    def test_exact_id_lookup_ranks_first(self) -> None:
        result = self.catalog.search("RLX-CAU-002", limit=1)
        self.assertEqual(result[0].entry.id, "RLX-CAU-002")
        self.assertEqual(result[0].match, "exact")

    def test_lexical_search(self) -> None:
        result = self.catalog.search("sampling limitation excluded group", limit=1)
        self.assertEqual(result[0].entry.id, "RLX-LIM-001")
        self.assertEqual(result[0].match, "lexical")

    def test_fuzzy_search(self) -> None:
        result = self.catalog.search("measurment limtation", limit=3)
        self.assertIn("RLX-LIM-002", [item.entry.id for item in result])

    def test_filters(self) -> None:
        results = self.catalog.search(
            "effect",
            function="causal_claim",
            evidence="direct",
            max_claim_strength="causal",
            risk="high",
        )
        self.assertTrue(results)
        self.assertTrue(all(result.entry.function == "causal_claim" for result in results))
        self.assertTrue(all(result.entry.evidence_requirement == "direct" for result in results))

    def test_filter_only_search(self) -> None:
        results = self.catalog.search("", function="define_scope")
        self.assertEqual(len(results), 4)

    def test_suggestions(self) -> None:
        suggestions = self.catalog.suggest("caus")
        self.assertIn("causal_claim", suggestions)

    def test_seeded_random_is_reproducible(self) -> None:
        first = self.catalog.random(seed="stable", function="identify_gap")
        second = self.catalog.random(seed="stable", function="identify_gap")
        self.assertEqual(first.id, second.id)

    def test_frozen_benchmark(self) -> None:
        benchmark = json.loads((ROOT / "benchmarks" / "search-v0.1.json").read_text(encoding="utf-8"))
        self.assertEqual(benchmark["status"], "frozen")
        failures = []
        for case in benchmark["cases"]:
            results = self.catalog.search(case["query"], limit=1)
            observed = results[0].entry.function if results else None
            if observed != case["expected_function"]:
                failures.append((case["id"], observed, results[0].entry.id if results else None))
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
