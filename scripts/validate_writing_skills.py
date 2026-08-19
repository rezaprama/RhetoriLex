"""Validate the clean-room writing-skills catalog and its interface translation."""

from __future__ import annotations

from collections import Counter
import re
from typing import Any


EXPECTED_GROUPS: dict[str, tuple[str, int]] = {
    "research-framing": ("academic", 11),
    "literature-writing": ("academic", 13),
    "argumentation": ("academic", 15),
    "thesis-and-dissertation": ("academic", 13),
    "publication-writing": ("academic", 12),
    "scientific-study-framing": ("scientific", 6),
    "methods-writing": ("scientific", 19),
    "results-writing": ("scientific", 17),
    "discussion-writing": ("scientific", 13),
    "scientific-claim-control": ("scientific", 11),
    "paraphrasing": ("paraphrasing", 14),
}

TOP_FIELDS = {
    "$schema",
    "format",
    "format_version",
    "release",
    "language",
    "count",
    "group_count",
    "provenance",
    "groups",
    "skills",
}
GROUP_FIELDS = {"id", "domain", "name", "description", "count", "canonical_en"}
SKILL_FIELDS = {
    "id",
    "slug",
    "domain",
    "group",
    "name",
    "description",
    "rhetorical_objective",
    "use_cases",
    "example",
    "related_phrase_functions",
    "related_skill_ids",
    "evidence_claim_warning",
    "canonical_en",
}
TRANSLATION_TOP_FIELDS = {
    "$schema",
    "format",
    "format_version",
    "release",
    "language",
    "canonical_language",
    "source",
    "count",
    "groups",
    "skills",
}
LABEL_FIELDS = {"id", "name", "description"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_ID_RE = re.compile(
    r"^writing\.(academic|scientific|paraphrasing)\.[a-z0-9_]+\.[a-z0-9_]+$"
)


def _object_fields(value: Any, expected: set[str], label: str, errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return False
    missing = expected - value.keys()
    extra = value.keys() - expected
    if missing:
        errors.append(f"{label} missing fields {sorted(missing)}")
    if extra:
        errors.append(f"{label} has unexpected fields {sorted(extra)}")
    return not missing


def _string(value: Any, label: str, errors: list[str], minimum: int) -> bool:
    if not isinstance(value, str):
        errors.append(f"{label} must be a string")
        return False
    if len(value.strip()) < minimum:
        errors.append(f"{label} must contain at least {minimum} characters")
        return False
    return True


def _string_array(
    value: Any,
    label: str,
    errors: list[str],
    *,
    minimum: int = 1,
) -> bool:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return False
    valid = True
    if len(value) < minimum:
        errors.append(f"{label} must contain at least {minimum} item(s)")
        valid = False
    if not all(isinstance(item, str) and len(item.strip()) >= 3 for item in value):
        errors.append(f"{label} items must be strings with at least three characters")
        valid = False
    if len(value) != len(set(item for item in value if isinstance(item, str))):
        errors.append(f"{label} items must be unique")
        valid = False
    return valid


def _translation_labels(
    value: Any,
    label: str,
    expected_ids: list[str],
    errors: list[str],
) -> None:
    if not isinstance(value, list):
        errors.append(f"translation {label} must be an array")
        return
    ids: list[str] = []
    for index, item in enumerate(value):
        item_label = f"translation {label}[{index}]"
        if not _object_fields(item, LABEL_FIELDS, item_label, errors):
            continue
        item_id = item.get("id")
        if _string(item_id, f"{item_label}.id", errors, 3):
            ids.append(item_id)
        _string(item.get("name"), f"{item_label}.name", errors, 3)
        _string(item.get("description"), f"{item_label}.description", errors, 15)
    if ids != expected_ids:
        errors.append(f"translation {label} ids must exactly match canonical order")
    if len(ids) != len(set(ids)):
        errors.append(f"translation {label} ids must be unique")


def validate_writing_skills(
    catalog: dict[str, Any],
    translation: dict[str, Any],
    taxonomy: dict[str, Any],
) -> list[str]:
    """Return all catalog, reference, route, and translation contract errors."""

    errors: list[str] = []
    if not _object_fields(catalog, TOP_FIELDS, "writing skills", errors):
        return errors
    constants = {
        "$schema": "../schema/writing-skills.v1.schema.json",
        "format": "rhetorilex-writing-skills",
        "format_version": "1.0.0",
        "release": "0.2.0",
        "language": "en",
        "count": 144,
        "group_count": 11,
    }
    for field, expected in constants.items():
        value = catalog.get(field)
        if type(value) is not type(expected) or value != expected:
            errors.append(f"writing skills {field} must equal {expected!r}")

    provenance = catalog.get("provenance")
    provenance_fields = {"method", "author", "source_reuse", "restricted_source_used"}
    if _object_fields(provenance, provenance_fields, "writing skills provenance", errors):
        if provenance.get("method") != "original_editorial":
            errors.append("writing skills provenance.method must equal 'original_editorial'")
        _string(provenance.get("author"), "writing skills provenance.author", errors, 3)
        for field in ("source_reuse", "restricted_source_used"):
            value = provenance.get(field)
            if type(value) is not bool or value is not False:
                errors.append(f"writing skills provenance.{field} must equal false")

    group_rows = catalog.get("groups")
    group_ids: list[str] = []
    if not isinstance(group_rows, list):
        errors.append("writing skills groups must be an array")
        group_rows = []
    for index, group in enumerate(group_rows):
        label = f"writing skills groups[{index}]"
        if not _object_fields(group, GROUP_FIELDS, label, errors):
            continue
        group_id = group.get("id")
        if not isinstance(group_id, str) or SLUG_RE.fullmatch(group_id) is None:
            errors.append(f"{label}.id has invalid slug format")
            continue
        group_ids.append(group_id)
        if group_id not in EXPECTED_GROUPS:
            errors.append(f"{label}.id has unknown group {group_id!r}")
            continue
        domain, expected_count = EXPECTED_GROUPS[group_id]
        if group.get("domain") != domain:
            errors.append(f"{label}.domain must equal {domain!r}")
        if type(group.get("count")) is not int or group.get("count") != expected_count:
            errors.append(f"{label}.count must equal {expected_count}")
        _string(group.get("name"), f"{label}.name", errors, 3)
        _string(group.get("description"), f"{label}.description", errors, 20)
        expected_route = f"/en/writing-skills/{group_id}/"
        if group.get("canonical_en") != expected_route:
            errors.append(f"{label}.canonical_en must equal {expected_route!r}")
    if group_ids != list(EXPECTED_GROUPS):
        errors.append("writing skills groups must exactly match the required ordered group catalog")
    if len(group_ids) != len(set(group_ids)):
        errors.append("writing skills group ids must be unique")

    function_ids = {
        item.get("id")
        for item in taxonomy.get("rhetorical_functions", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    skill_rows = catalog.get("skills")
    if not isinstance(skill_rows, list):
        errors.append("writing skills skills must be an array")
        skill_rows = []
    skill_ids: list[str] = []
    slugs: list[str] = []
    routes: list[str] = []
    group_counts: Counter[str] = Counter()
    pending_related: list[tuple[str, list[str]]] = []
    for index, skill in enumerate(skill_rows):
        label = f"writing skills skills[{index}]"
        if not _object_fields(skill, SKILL_FIELDS, label, errors):
            continue
        skill_id = skill.get("id")
        slug = skill.get("slug")
        group_id = skill.get("group")
        domain = skill.get("domain")
        if not isinstance(skill_id, str) or SKILL_ID_RE.fullmatch(skill_id) is None:
            errors.append(f"{label}.id has invalid format")
        else:
            skill_ids.append(skill_id)
        if not isinstance(slug, str) or SLUG_RE.fullmatch(slug) is None:
            errors.append(f"{label}.slug has invalid format")
        else:
            slugs.append(slug)
        if not isinstance(group_id, str) or group_id not in EXPECTED_GROUPS:
            errors.append(f"{label}.group has unknown value {group_id!r}")
        else:
            group_counts[group_id] += 1
            expected_domain = EXPECTED_GROUPS[group_id][0]
            if domain != expected_domain:
                errors.append(f"{label}.domain must equal {expected_domain!r}")
            if isinstance(skill_id, str):
                prefix = f"writing.{expected_domain}.{group_id.replace('-', '_')}."
                if not skill_id.startswith(prefix):
                    errors.append(f"{label}.id must start with {prefix!r}")
        _string(skill.get("name"), f"{label}.name", errors, 3)
        _string(skill.get("description"), f"{label}.description", errors, 20)
        _string(skill.get("rhetorical_objective"), f"{label}.rhetorical_objective", errors, 15)
        _string(skill.get("example"), f"{label}.example", errors, 15)
        _string(skill.get("evidence_claim_warning"), f"{label}.evidence_claim_warning", errors, 20)
        _string_array(skill.get("use_cases"), f"{label}.use_cases", errors)
        functions = skill.get("related_phrase_functions")
        if _string_array(functions, f"{label}.related_phrase_functions", errors):
            unknown = set(functions) - function_ids
            if unknown:
                errors.append(f"{label}.related_phrase_functions has unknown ids {sorted(unknown)}")
        related = skill.get("related_skill_ids")
        if _string_array(related, f"{label}.related_skill_ids", errors):
            pending_related.append((skill_id if isinstance(skill_id, str) else label, related))
        route = skill.get("canonical_en")
        if isinstance(group_id, str) and isinstance(slug, str):
            expected_route = f"/en/writing-skills/{group_id}/#{slug}"
            if route != expected_route:
                errors.append(f"{label}.canonical_en must equal {expected_route!r}")
        if isinstance(route, str):
            routes.append(route)

    for label, values in (("ids", skill_ids), ("slugs", slugs), ("canonical routes", routes)):
        if len(values) != len(set(values)):
            errors.append(f"writing skills {label} must be globally unique")
    if len(skill_rows) != 144:
        errors.append(f"writing skills must contain 144 skills; found {len(skill_rows)}")
    if catalog.get("count") != len(skill_rows):
        errors.append("writing skills count must match skills array length")
    for group_id, (_, expected_count) in EXPECTED_GROUPS.items():
        if group_counts[group_id] != expected_count:
            errors.append(
                f"writing skills group {group_id!r} must contain {expected_count}; "
                f"found {group_counts[group_id]}"
            )
    known_skill_ids = set(skill_ids)
    for skill_id, related in pending_related:
        unknown = set(related) - known_skill_ids
        if unknown:
            errors.append(f"{skill_id}: related_skill_ids has unknown ids {sorted(unknown)}")
        if skill_id in related:
            errors.append(f"{skill_id}: related_skill_ids must not reference itself")

    if not _object_fields(translation, TRANSLATION_TOP_FIELDS, "writing skills translation", errors):
        return errors
    translation_constants = {
        "$schema": "../schema/writing-skills-translation.v1.schema.json",
        "format": "rhetorilex-writing-skills-translation",
        "format_version": "1.0.0",
        "release": "0.2.0",
        "language": "id",
        "canonical_language": "en",
        "source": "../editorial/writing-skills.v1.json",
        "count": 144,
    }
    for field, expected in translation_constants.items():
        value = translation.get(field)
        if type(value) is not type(expected) or value != expected:
            errors.append(f"writing skills translation {field} must equal {expected!r}")
    _translation_labels(translation.get("groups"), "groups", group_ids, errors)
    _translation_labels(translation.get("skills"), "skills", skill_ids, errors)
    return errors

