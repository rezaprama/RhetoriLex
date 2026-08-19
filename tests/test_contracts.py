from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rhetorilex import Catalog, check_entry_contract  # noqa: E402


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = Catalog.load()

    def test_all_bundled_entries_pass_contract(self) -> None:
        failures = {
            entry.id: check_entry_contract(entry, self.catalog.contract)
            for entry in self.catalog.entries
            if check_entry_contract(entry, self.catalog.contract)
        }
        self.assertEqual(failures, {})

    def test_contract_rejects_unsupported_causal_claim(self) -> None:
        original = self.catalog.get("RLX-CAU-001")
        broken = replace(original, evidence_requirement="contextual", causal_design_required=False)
        codes = {issue.code for issue in check_entry_contract(broken, self.catalog.contract)}
        self.assertIn("insufficient_evidence", codes)
        self.assertIn("causal_design_missing", codes)

    def test_contract_rejects_placeholder_drift(self) -> None:
        original = self.catalog.get("RLX-POS-001")
        broken = replace(original, placeholders=("claim",))
        codes = {issue.code for issue in check_entry_contract(broken, self.catalog.contract)}
        self.assertIn("placeholder_mismatch", codes)


if __name__ == "__main__":
    unittest.main()
