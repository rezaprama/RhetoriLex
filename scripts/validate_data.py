"""Validate canonical RhetoriLex data without third-party packages."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import string
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "data" / "canonical" / "catalog.v1.jsonl"
DEFAULT_TAXONOMY = ROOT / "data" / "taxonomy" / "taxonomy.v1.json"
DEFAULT_CONTRACT = ROOT / "data" / "contracts" / "evidence-claim.v1.json"
ID_RE = re.compile(r"^RLX-[A-Z]{3}-[0-9]{3}$")
PLACEHOLDER_RE = re.compile(r"^[a-z][a-z0-9_]*$")

REQUIRED_FIELDS = {
    "id",
    "function",
    "title",
    "template",
    "description",
    "stage",
    "disciplines",
    "claim_strength",
    "evidence_requirement",
    "causal_design_required",
    "placeholders",
    "keywords",
    "notes",
    "risk",
    "provenance",
    "version",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def load_entries(path: Path = DEFAULT_CATALOG) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected JSON object")
            entries.append(value)
    return entries


def placeholders(template: str) -> set[str]:
    return {
        field
        for _, field, _, _ in string.Formatter().parse(template)
        if field is not None and field != ""
    }


def _ids(items: Iterable[dict[str, Any]]) -> set[str]:
    return {str(item["id"]) for item in items}


def _has_duplicates(values: list[Any]) -> bool:
    """Compare JSON values deterministically, including unhashable arrays/objects."""
    identities = [
        f"{type(value).__name__}:{json.dumps(value, ensure_ascii=False, sort_keys=True)}"
        for value in values
    ]
    return len(identities) != len(set(identities))


def _validate_string(
    entry_id: str,
    field_name: str,
    value: Any,
    errors: list[str],
    *,
    minimum: int = 0,
) -> bool:
    if not isinstance(value, str):
        errors.append(f"{entry_id}: {field_name} must be a string")
        return False
    if len(value) < minimum:
        errors.append(f"{entry_id}: {field_name} must contain at least {minimum} characters")
        return False
    return True


def _validate_string_array(
    entry_id: str,
    field_name: str,
    value: Any,
    errors: list[str],
    *,
    minimum_items: int = 0,
    item_minimum: int = 0,
    item_pattern: re.Pattern[str] | None = None,
    allowed: set[str] | None = None,
) -> bool:
    if not isinstance(value, list):
        errors.append(f"{entry_id}: {field_name} must be an array")
        return False
    valid = True
    if len(value) < minimum_items:
        errors.append(f"{entry_id}: {field_name} must contain at least {minimum_items} item(s)")
        valid = False
    if _has_duplicates(value):
        errors.append(f"{entry_id}: {field_name} items must be unique")
        valid = False
    for index, item in enumerate(value):
        if not isinstance(item, str):
            errors.append(f"{entry_id}: {field_name}[{index}] must be a string")
            valid = False
            continue
        if len(item) < item_minimum:
            errors.append(
                f"{entry_id}: {field_name}[{index}] must contain at least {item_minimum} characters"
            )
            valid = False
        if item_pattern is not None and item_pattern.fullmatch(item) is None:
            errors.append(f"{entry_id}: {field_name}[{index}] has invalid format")
            valid = False
        if allowed is not None and item not in allowed:
            errors.append(f"{entry_id}: {field_name}[{index}] has unknown value {item!r}")
            valid = False
    return valid


def validate(
    entries: list[dict[str, Any]],
    taxonomy: dict[str, Any],
    contract: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    functions = _ids(taxonomy["rhetorical_functions"])
    strengths = _ids(taxonomy["claim_strengths"])
    evidence_values = _ids(taxonomy["evidence_requirements"])
    risks = _ids(taxonomy["risk_levels"])
    stages = set(taxonomy["stages"])
    disciplines = set(taxonomy["disciplines"])
    evidence_order = contract["evidence_order"]
    slot_names = set(contract["evidence_slot_names"])
    seen: Counter[str] = Counter()

    for row_number, row in enumerate(entries, start=1):
        if not isinstance(row, dict):
            errors.append(f"entry-{row_number}: entry must be an object")
            continue
        entry = dict(row)
        raw_id = entry.get("id")
        entry_id = raw_id if isinstance(raw_id, str) else f"entry-{row_number}"
        if isinstance(raw_id, str):
            seen[raw_id] += 1

        missing = REQUIRED_FIELDS - entry.keys()
        extra = entry.keys() - REQUIRED_FIELDS
        if missing:
            errors.append(f"{entry_id}: missing fields {sorted(missing)}")
        if extra:
            errors.append(f"{entry_id}: unexpected fields {sorted(extra)}")
        if missing:
            continue

        if not isinstance(raw_id, str):
            errors.append(f"{entry_id}: id must be a string")
        elif ID_RE.fullmatch(raw_id) is None:
            errors.append(f"{entry_id}: id has invalid format")

        enum_fields = {
            "function": functions,
            "claim_strength": strengths,
            "evidence_requirement": evidence_values,
            "risk": risks,
            "stage": stages,
        }
        valid_enums: dict[str, bool] = {}
        for field_name, allowed in enum_fields.items():
            value = entry[field_name]
            if not isinstance(value, str):
                errors.append(f"{entry_id}: {field_name} must be a string")
                valid_enums[field_name] = False
            elif value not in allowed:
                errors.append(f"{entry_id}: {field_name} has unknown value {value!r}")
                valid_enums[field_name] = False
            else:
                valid_enums[field_name] = True

        title_valid = _validate_string(entry_id, "title", entry["title"], errors, minimum=3)
        template_valid = _validate_string(
            entry_id, "template", entry["template"], errors, minimum=10
        )
        description_valid = _validate_string(
            entry_id, "description", entry["description"], errors, minimum=10
        )
        notes_valid = _validate_string(entry_id, "notes", entry["notes"], errors, minimum=5)
        _ = (title_valid, description_valid, notes_valid)

        disciplines_valid = _validate_string_array(
            entry_id,
            "disciplines",
            entry["disciplines"],
            errors,
            minimum_items=1,
            allowed=disciplines,
        )
        placeholders_valid = _validate_string_array(
            entry_id,
            "placeholders",
            entry["placeholders"],
            errors,
            item_pattern=PLACEHOLDER_RE,
        )
        _validate_string_array(
            entry_id,
            "keywords",
            entry["keywords"],
            errors,
            minimum_items=2,
            item_minimum=2,
        )
        _ = disciplines_valid

        causal_flag_valid = type(entry["causal_design_required"]) is bool
        if not causal_flag_valid:
            errors.append(f"{entry_id}: causal_design_required must be a boolean")

        version = entry["version"]
        if type(version) is not int:
            errors.append(f"{entry_id}: version must be an integer (booleans are not integers)")
        elif version < 1:
            errors.append(f"{entry_id}: version must be at least 1")

        provenance = entry["provenance"]
        if not isinstance(provenance, dict):
            errors.append(f"{entry_id}: provenance must be an object")
        else:
            required_provenance = {"method", "author", "source_reuse"}
            provenance_missing = required_provenance - provenance.keys()
            provenance_extra = provenance.keys() - required_provenance
            if provenance_missing:
                errors.append(
                    f"{entry_id}: provenance missing fields {sorted(provenance_missing)}"
                )
            if provenance_extra:
                errors.append(
                    f"{entry_id}: provenance has unexpected fields {sorted(provenance_extra)}"
                )
            if "method" in provenance:
                method = provenance["method"]
                if not isinstance(method, str):
                    errors.append(f"{entry_id}: provenance.method must be a string")
                elif method != "original_editorial":
                    errors.append(
                        f"{entry_id}: provenance.method must equal 'original_editorial'"
                    )
            if "author" in provenance:
                _validate_string(
                    entry_id, "provenance.author", provenance["author"], errors, minimum=3
                )
            if "source_reuse" in provenance:
                source_reuse = provenance["source_reuse"]
                if type(source_reuse) is not bool:
                    errors.append(f"{entry_id}: provenance.source_reuse must be a boolean")
                elif source_reuse is not False:
                    errors.append(f"{entry_id}: provenance.source_reuse must equal false")

        actual_slots: set[str] | None = None
        if template_valid:
            try:
                actual_slots = placeholders(entry["template"])
            except ValueError as exc:
                errors.append(f"{entry_id}: template has invalid placeholder syntax: {exc}")
        if placeholders_valid and actual_slots is not None:
            declared_slots = set(entry["placeholders"])
            if actual_slots != declared_slots:
                errors.append(
                    f"{entry_id}: placeholder mismatch declared={sorted(declared_slots)} "
                    f"actual={sorted(actual_slots)}"
                )
        if (
            valid_enums["evidence_requirement"]
            and entry["evidence_requirement"] not in {"none", "contextual"}
            and actual_slots is not None
            and not (actual_slots & slot_names)
        ):
            errors.append(f"{entry_id}: evidence-bearing template lacks evidence slot")

        if valid_enums["claim_strength"] and valid_enums["evidence_requirement"]:
            rule = contract["claim_strength_rules"][entry["claim_strength"]]
            minimum = evidence_order.index(rule["minimum_evidence"])
            actual = evidence_order.index(entry["evidence_requirement"])
            if actual < minimum:
                errors.append(
                    f"{entry_id}: {entry['claim_strength']} requires at least {rule['minimum_evidence']}"
                )
            if rule["causal_design_required"] and causal_flag_valid and not entry[
                "causal_design_required"
            ]:
                errors.append(f"{entry_id}: causal design flag required")
        if (
            causal_flag_valid
            and entry["causal_design_required"]
            and valid_enums["risk"]
            and entry["risk"] != "high"
        ):
            errors.append(f"{entry_id}: causal design requires high risk")

    duplicates = sorted(key for key, count in seen.items() if count > 1)
    if duplicates:
        errors.append(f"duplicate ids: {duplicates}")
    if not 36 <= len(entries) <= 60:
        errors.append(f"catalog must contain 36-60 entries; found {len(entries)}")
    counts = Counter(
        row.get("function")
        for row in entries
        if isinstance(row, dict) and isinstance(row.get("function"), str)
    )
    missing_functions = sorted(functions - counts.keys())
    if missing_functions:
        errors.append(f"functions without entries: {missing_functions}")
    thin_functions = sorted(key for key, count in counts.items() if key in functions and count < 3)
    if thin_functions:
        errors.append(f"functions need at least three entries: {thin_functions}")
    return errors

def validate_paths(
    catalog_path: Path = DEFAULT_CATALOG,
    taxonomy_path: Path = DEFAULT_TAXONOMY,
    contract_path: Path = DEFAULT_CONTRACT,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], list[str]]:
    entries = load_entries(catalog_path)
    taxonomy = load_json(taxonomy_path)
    contract = load_json(contract_path)
    return entries, taxonomy, contract, validate(entries, taxonomy, contract)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--taxonomy", type=Path, default=DEFAULT_TAXONOMY)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    args = parser.parse_args(argv)
    try:
        entries, _, _, errors = validate_paths(args.catalog, args.taxonomy, args.contract)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(f"invalid: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"valid: {len(entries)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
