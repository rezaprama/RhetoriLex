from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_writing_skills import EXPECTED_GROUPS, validate_writing_skills  # noqa: E402


EXPECTED_NAMES = {
    "research-framing": """
Establishing a research context
Introducing a topic
Establishing significance
Defining a research problem
Identifying a research gap
Stating research aims
Writing research questions
Stating hypotheses
Describing scope
Stating contributions
Describing novelty cautiously
""",
    "literature-writing": """
Introducing previous studies
Synthesising literature
Comparing studies
Contrasting studies
Describing scholarly consensus
Describing scholarly disagreement
Identifying limitations in prior work
Critiquing previous research
Qualifying criticism
Establishing a literature gap
Writing related work
Transitioning between sources
Citation-integrated writing
""",
    "argumentation": """
Making an academic claim
Supporting a claim
Qualifying a claim
Hedging
Emphasising cautiously
Conceding a point
Presenting counterarguments
Drawing distinctions
Expressing agreement
Expressing disagreement
Defining concepts
Classifying concepts
Giving examples
Drawing comparisons
Explaining implications
""",
    "thesis-and-dissertation": """
Thesis introduction
Chapter introduction
Literature review
Conceptual framework
Theoretical framework
Methodology chapter
Findings chapter
Discussion chapter
Chapter summary
General conclusion
Recommendations
Future research
Thesis limitations
""",
    "publication-writing": """
Academic abstract
Research proposal
Journal manuscript
Conference paper
Cover letter
Reviewer response
Revision response
Author contribution statement
Data availability language
Ethics statement language
Conflict-of-interest language
Acknowledgements
""",
    "scientific-study-framing": """
Scientific background
Scientific rationale
Research objective
Hypothesis language
Knowledge gap
Scientific contribution
""",
    "methods-writing": """
Study design
Study setting
Participants
Sampling
Inclusion criteria
Exclusion criteria
Materials
Instruments
Experimental procedures
Variables
Measurements
Data collection
Statistical methods
Qualitative methods
Model specification
Sensitivity analysis
Validation
Reproducibility
Ethical approval
""",
    "results-writing": """
Introducing results
Reporting descriptive statistics
Reporting comparisons
Reporting associations
Reporting effects
Reporting uncertainty
Confidence intervals
Statistical significance
Non-significant findings
Null findings
Trends
Subgroup results
Sensitivity results
Robustness results
Unexpected findings
Referring to tables
Referring to figures
""",
    "discussion-writing": """
Summarising principal findings
Interpreting findings
Comparing findings with literature
Explaining possible mechanisms
Presenting competing explanations
Discussing uncertainty
Discussing limitations
Discussing strengths
Discussing generalisability
Theoretical implications
Practical implications
Policy implications
Future research
""",
    "scientific-claim-control": """
Association vs causation
Correlation language
Prediction language
Causal language
Evidence strength
Hedging scientific claims
Avoiding overclaiming
Interpreting null results
Effect size language
Uncertainty language
Scope and generalisation
""",
    "paraphrasing": """
Meaning-preserving paraphrase
Structural paraphrase
Academic paraphrase
Scientific paraphrase
Concision
Sentence restructuring
Citation-preserving rewrite
Number-preserving rewrite
Claim-strength-preserving rewrite
Cautious rewriting
Academic register
Removing unnecessary verbosity
Reducing repetition
Improving logical flow
""",
}
EXPECTED_NAMES = {
    group: [line for line in block.strip().splitlines() if line]
    for group, block in EXPECTED_NAMES.items()
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain an object")
    return value


class WritingSkillCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = load(ROOT / "data" / "editorial" / "writing-skills.v1.json")
        cls.translation = load(
            ROOT / "data" / "translations" / "writing-skills.id.v1.json"
        )
        cls.taxonomy = load(ROOT / "data" / "taxonomy" / "taxonomy.v1.1.json")

    def test_exact_phase2_inventory_and_group_counts(self) -> None:
        errors = validate_writing_skills(
            self.catalog, self.translation, self.taxonomy
        )
        self.assertEqual(errors, [])
        self.assertEqual(self.catalog["count"], 144)
        self.assertEqual(
            [group["id"] for group in self.catalog["groups"]],
            list(EXPECTED_GROUPS),
        )
        by_group: dict[str, list[str]] = {group: [] for group in EXPECTED_GROUPS}
        for skill in self.catalog["skills"]:
            by_group[skill["group"]].append(skill["name"])
        self.assertEqual(by_group, EXPECTED_NAMES)
        counts = Counter(skill["domain"] for skill in self.catalog["skills"])
        self.assertEqual(
            counts,
            {"academic": 64, "scientific": 66, "paraphrasing": 14},
        )

    def test_records_are_substantive_original_and_referentially_complete(self) -> None:
        function_ids = {
            item["id"] for item in self.taxonomy["rhetorical_functions"]
        }
        skill_ids = {item["id"] for item in self.catalog["skills"]}
        self.assertEqual(len(skill_ids), 144)
        self.assertEqual(len({item["slug"] for item in self.catalog["skills"]}), 144)
        self.assertEqual(
            self.catalog["provenance"],
            {
                "method": "original_editorial",
                "author": "Reza Prama Arviandi",
                "source_reuse": False,
                "restricted_source_used": False,
            },
        )
        for skill in self.catalog["skills"]:
            with self.subTest(skill=skill["id"]):
                self.assertGreaterEqual(len(skill["example"]), 15)
                self.assertTrue(set(skill["related_phrase_functions"]) <= function_ids)
                self.assertTrue(set(skill["related_skill_ids"]) <= skill_ids)
                self.assertNotIn(skill["id"], skill["related_skill_ids"])
                self.assertEqual(
                    skill["canonical_en"],
                    f"/en/writing-skills/{skill['group']}/#{skill['slug']}",
                )

    def test_indonesian_file_is_interface_only_and_has_exact_id_parity(self) -> None:
        self.assertEqual(
            [row["id"] for row in self.translation["groups"]],
            [row["id"] for row in self.catalog["groups"]],
        )
        self.assertEqual(
            [row["id"] for row in self.translation["skills"]],
            [row["id"] for row in self.catalog["skills"]],
        )
        for row in self.translation["skills"]:
            self.assertEqual(set(row), {"id", "name", "description"})
            self.assertNotIn("example", row)

    def errors_for(self, catalog_mutation=None, translation_mutation=None) -> list[str]:
        catalog = deepcopy(self.catalog)
        translation = deepcopy(self.translation)
        if catalog_mutation is not None:
            catalog_mutation(catalog)
        if translation_mutation is not None:
            translation_mutation(translation)
        return validate_writing_skills(catalog, translation, self.taxonomy)

    def assert_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors}",
        )

    def test_rejects_duplicate_slug_bad_route_and_unknown_references(self) -> None:
        cases = [
            (
                lambda data: data["skills"][1].__setitem__(
                    "slug", data["skills"][0]["slug"]
                ),
                "slugs must be globally unique",
            ),
            (
                lambda data: data["skills"][0].__setitem__(
                    "canonical_en", "/en/writing-skills/wrong/#route"
                ),
                "canonical_en must equal",
            ),
            (
                lambda data: data["skills"][0].__setitem__(
                    "related_phrase_functions", ["unknown_function"]
                ),
                "related_phrase_functions has unknown ids",
            ),
            (
                lambda data: data["skills"][0].__setitem__(
                    "related_skill_ids", ["writing.academic.unknown.missing"]
                ),
                "related_skill_ids has unknown ids",
            ),
            (
                lambda data: data["skills"][0].__setitem__("unexpected", True),
                "has unexpected fields ['unexpected']",
            ),
        ]
        for mutation, expected in cases:
            with self.subTest(expected=expected):
                self.assert_error(self.errors_for(mutation), expected)

    def test_rejects_wrong_types_provenance_and_translation_drift(self) -> None:
        self.assert_error(
            self.errors_for(lambda data: data.__setitem__("count", True)),
            "count must equal 144",
        )
        self.assert_error(
            self.errors_for(
                lambda data: data["provenance"].__setitem__(
                    "restricted_source_used", True
                )
            ),
            "restricted_source_used must equal false",
        )
        self.assert_error(
            self.errors_for(
                translation_mutation=lambda data: data["skills"][0].__setitem__(
                    "example", "Translated examples are forbidden here."
                )
            ),
            "has unexpected fields ['example']",
        )
        self.assert_error(
            self.errors_for(
                translation_mutation=lambda data: data["skills"].pop()
            ),
            "ids must exactly match canonical order",
        )


if __name__ == "__main__":
    unittest.main()

