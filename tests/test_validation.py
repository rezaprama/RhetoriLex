from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_data import validate, validate_paths  # noqa: E402


class ValidationTests(unittest.TestCase):
    def test_canonical_catalog_is_valid(self) -> None:
        entries, taxonomy, contract, errors = validate_paths()
        self.assertEqual(errors, [])
        self.assertEqual(len(entries), 96)
        self.assertEqual(len(taxonomy["rhetorical_functions"]), 24)
        self.assertEqual(len(taxonomy["domains"]), 10)
        self.assertEqual(len(taxonomy["skill_areas"]), 13)
        self.assertEqual(set(contract["claim_strength_rules"]), {"tentative", "bounded", "assertive", "causal"})

    def test_all_schemas_are_valid_json(self) -> None:
        schemas = sorted((ROOT / "data" / "schema").glob("*.json"))
        self.assertGreaterEqual(len(schemas), 3)
        for path in schemas:
            with self.subTest(path=path.name):
                value = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(value["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_canonical_manifest_is_single_source_map(self) -> None:
        canonical = ROOT / "data" / "canonical"
        manifest = json.loads(
            (canonical / "catalog-manifest.v2.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["release_version"], "0.2.0")
        self.assertEqual(manifest["entry_count"], 96)
        self.assertEqual(
            manifest["shards"], ["catalog.v1.jsonl", "catalog.phase2.jsonl"]
        )
        self.assertEqual(
            sorted(manifest["shards"]),
            sorted(path.name for path in canonical.glob("*.jsonl")),
        )
        self.assertEqual(
            manifest["translation_manifest"], "../translations/manifest.v2.json"
        )
    def test_every_entry_has_original_editorial_provenance(self) -> None:
        entries, _, _, _ = validate_paths()
        for row in entries:
            with self.subTest(entry=row["id"]):
                self.assertEqual(row["provenance"]["method"], "original_editorial")
                self.assertIs(row["provenance"]["source_reuse"], False)


class MalformedEntryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.entries, cls.taxonomy, cls.contract, errors = validate_paths()
        if errors:
            raise AssertionError(errors)

    def errors_for(self, mutation) -> list[str]:
        entries = deepcopy(self.entries)
        mutation(entries[0])
        return validate(entries, self.taxonomy, self.contract)

    def assert_has_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in errors: {errors}",
        )

    def test_json_scalar_types_are_exact(self) -> None:
        cases = [
            (
                lambda row: row.__setitem__("causal_design_required", "false"),
                "causal_design_required must be a boolean",
            ),
            (
                lambda row: row.__setitem__("version", "1"),
                "version must be an integer",
            ),
            (
                lambda row: row.__setitem__("version", True),
                "version must be an integer",
            ),
            (
                lambda row: row.__setitem__("version", 0),
                "version must be at least 1",
            ),
            (
                lambda row: row.__setitem__("id", 17),
                "id must be a string",
            ),
        ]
        for mutation, expected in cases:
            with self.subTest(expected=expected):
                self.assert_has_error(self.errors_for(mutation), expected)

    def test_array_items_patterns_lengths_and_uniqueness(self) -> None:
        cases = [
            (
                lambda row: row.__setitem__("placeholders", [7, "scope"]),
                "placeholders[0] must be a string",
            ),
            (
                lambda row: row.__setitem__("placeholders", ["Bad-Name", "scope"]),
                "placeholders[0] has invalid format",
            ),
            (
                lambda row: row.__setitem__("disciplines", ["general", "general"]),
                "disciplines items must be unique",
            ),
            (
                lambda row: row.__setitem__("keywords", ["x", "scope"]),
                "keywords[0] must contain at least 2 characters",
            ),
            (
                lambda row: row.__setitem__("disciplines", "general"),
                "disciplines must be an array",
            ),
        ]
        for mutation, expected in cases:
            with self.subTest(expected=expected):
                self.assert_has_error(self.errors_for(mutation), expected)

    def test_schema_string_minimum_lengths(self) -> None:
        cases = [
            (
                lambda row: row.__setitem__("title", "xy"),
                "title must contain at least 3 characters",
            ),
            (
                lambda row: row.__setitem__("template", "short"),
                "template must contain at least 10 characters",
            ),
            (
                lambda row: row.__setitem__("description", "tiny"),
                "description must contain at least 10 characters",
            ),
            (
                lambda row: row.__setitem__("notes", "no"),
                "notes must contain at least 5 characters",
            ),
        ]
        for mutation, expected in cases:
            with self.subTest(expected=expected):
                self.assert_has_error(self.errors_for(mutation), expected)

    def test_enums_patterns_and_additional_properties(self) -> None:
        cases = [
            (
                lambda row: row.__setitem__("function", "unknown_function"),
                "function has unknown value",
            ),
            (
                lambda row: row.__setitem__("id", "bad-id"),
                "id has invalid format",
            ),
            (
                lambda row: row.__setitem__("unexpected", "forbidden"),
                "unexpected fields ['unexpected']",
            ),
        ]
        for mutation, expected in cases:
            with self.subTest(expected=expected):
                self.assert_has_error(self.errors_for(mutation), expected)

    def test_provenance_nested_schema(self) -> None:
        def malformed(row: dict) -> None:
            row["provenance"] = {
                "method": 1,
                "author": "x",
                "source_reuse": 0,
                "unexpected": True,
            }

        errors = self.errors_for(malformed)
        for expected in (
            "provenance has unexpected fields ['unexpected']",
            "provenance.method must be a string",
            "provenance.author must contain at least 3 characters",
            "provenance.source_reuse must be a boolean",
        ):
            self.assert_has_error(errors, expected)

        missing_errors = self.errors_for(
            lambda row: row.__setitem__(
                "provenance", {"method": "original_editorial", "author": "Author"}
            )
        )
        self.assert_has_error(
            missing_errors, "provenance missing fields ['source_reuse']"
        )

if __name__ == "__main__":
    unittest.main()
