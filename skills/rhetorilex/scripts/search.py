#!/usr/bin/env python3
"""Search bundled clean-room patterns and writing skills without dependencies."""

from __future__ import annotations

import argparse
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
from typing import Any


TOKEN_RE = re.compile(r"[a-z0-9]+")
STRENGTH = {"tentative": 0, "bounded": 1, "assertive": 2, "causal": 3}
ASSETS = Path(__file__).resolve().parents[1] / "assets"


def tokens(value: str) -> set[str]:
    return set(TOKEN_RE.findall(value.casefold()))


def load_json(name: str) -> Any:
    path = ASSETS / name
    if not path.is_file():
        raise SystemExit(f"Required asset not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_patterns() -> list[dict[str, Any]]:
    payload = load_json("patterns.json")
    records = payload if isinstance(payload, list) else payload.get("entries", [])
    if not records:
        raise SystemExit(f"No patterns found in {ASSETS / 'patterns.json'}")
    return records


def load_writing_catalog() -> dict[str, Any]:
    payload = load_json("writing-skills.json")
    records = payload.get("skills", []) if isinstance(payload, dict) else []
    if not records:
        raise SystemExit(f"No writing skills found in {ASSETS / 'writing-skills.json'}")
    return payload


def localized_skill_labels(language: str) -> dict[str, dict[str, str]]:
    if language == "en":
        return {}
    payload = load_json("writing-skills.id.json")
    return {
        row["id"]: {"name": row["name"], "description": row["description"]}
        for row in payload.get("skills", [])
    }


def compatible(row: dict[str, Any], args: argparse.Namespace) -> bool:
    if args.function and row["function"] != args.function:
        return False
    if args.section and row["stage"] not in {args.section, "general"}:
        return False
    if args.evidence and row["evidence_requirement"] != args.evidence:
        return False
    if (
        args.discipline
        and args.discipline not in row["disciplines"]
        and "general" not in row["disciplines"]
    ):
        return False
    if args.domain and args.domain not in row.get("domains", []):
        return False
    if args.skill_area and args.skill_area not in row.get("skill_areas", []):
        return False
    if args.risk and row["risk"] != args.risk:
        return False
    if (
        args.max_claim_strength
        and STRENGTH[row["claim_strength"]] > STRENGTH[args.max_claim_strength]
    ):
        return False
    return True


def score(row: dict[str, Any], query: str) -> float:
    fields = [
        row["id"],
        row["title"],
        row["template"],
        row["description"],
        row["function"],
        row["stage"],
        " ".join(row["keywords"]),
        " ".join(row.get("domains", [])),
        " ".join(row.get("skill_areas", [])),
    ]
    aliases = " ".join(row.get("search_aliases", []))
    haystack = " ".join(fields).casefold()
    normalized = query.casefold().strip()
    if not normalized:
        return 1.0
    query_tokens = tokens(query)
    core_overlap = len(query_tokens & tokens(haystack))
    alias_overlap = len(query_tokens & tokens(aliases))
    lexical = 58 * core_overlap / max(1, len(query_tokens))
    alias_score = 62 * alias_overlap / max(1, len(query_tokens))
    if normalized in haystack:
        lexical += 18
    if normalized in aliases.casefold():
        alias_score += 24
    fuzzy = max(
        SequenceMatcher(None, normalized, value.casefold()).ratio()
        for value in [*fields, aliases]
    ) * 20
    return lexical + alias_score + fuzzy


def writing_skill_score(
    row: dict[str, Any],
    query: str,
    localized: dict[str, dict[str, str]],
) -> float:
    interface = localized.get(row["id"], {})
    fields = [
        row["id"],
        row["slug"],
        row["group"],
        row["name"],
        row["description"],
        row["rhetorical_objective"],
        " ".join(row["use_cases"]),
        " ".join(row["related_phrase_functions"]),
        interface.get("name", ""),
        interface.get("description", ""),
    ]
    normalized = query.casefold().strip()
    if not normalized:
        return 1.0
    exact_values = {row["id"].casefold(), row["slug"].casefold(), row["name"].casefold()}
    if interface.get("name"):
        exact_values.add(interface["name"].casefold())
    exact = 150.0 if normalized in exact_values else 0.0
    haystack = " ".join(fields).casefold()
    overlap = len(tokens(query) & tokens(haystack))
    lexical = 70 * overlap / max(1, len(tokens(query)))
    if normalized in haystack:
        lexical += 40
    fuzzy = max(
        SequenceMatcher(None, normalized, field.casefold()).ratio()
        for field in fields
        if field
    ) * 25
    return exact + lexical + fuzzy


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "query",
        nargs="?",
        default="",
        help="writing intent, pattern purpose, skill name, or skill slug",
    )
    result.add_argument("--section", "--stage", dest="section")
    result.add_argument("--function")
    result.add_argument("--evidence")
    result.add_argument("--max-claim-strength", choices=tuple(STRENGTH))
    result.add_argument("--discipline")
    result.add_argument("--domain")
    result.add_argument("--skill-area")
    result.add_argument("--risk", choices=("low", "medium", "high"))
    result.add_argument(
        "--writing-skills",
        action="store_true",
        help="search the 144-skill guidance catalog instead of phrase patterns",
    )
    result.add_argument("--skill-group", help="writing-skill group slug")
    result.add_argument("--skill-slug", help="exact writing-skill slug")
    result.add_argument("--language", choices=("en", "id"), default="en")
    result.add_argument("--limit", type=int, default=3)
    result.add_argument("--json", action="store_true")
    listings = result.add_mutually_exclusive_group()
    listings.add_argument("--taxonomy", action="store_true")
    listings.add_argument("--list-sections", action="store_true")
    listings.add_argument("--list-functions", action="store_true")
    listings.add_argument("--list-disciplines", action="store_true")
    listings.add_argument("--list-domains", action="store_true")
    listings.add_argument("--list-skill-areas", action="store_true")
    listings.add_argument("--list-writing-skill-groups", action="store_true")
    return result


def listing(args: argparse.Namespace) -> Any | None:
    if args.list_writing_skill_groups:
        groups = load_writing_catalog()["groups"]
        if args.language == "en":
            return groups
        localized = {
            row["id"]: row for row in load_json("writing-skills.id.json").get("groups", [])
        }
        return [
            {**row, "localized_interface": localized.get(row["id"])}
            for row in groups
        ]
    if not any(
        (
            args.taxonomy,
            args.list_sections,
            args.list_functions,
            args.list_disciplines,
            args.list_domains,
            args.list_skill_areas,
        )
    ):
        return None
    taxonomy = load_json("taxonomy.json")
    if args.taxonomy:
        return taxonomy
    if args.list_sections:
        return taxonomy["stages"]
    if args.list_functions:
        return taxonomy["rhetorical_functions"]
    if args.list_disciplines:
        return taxonomy["disciplines"]
    if args.list_domains:
        return taxonomy["domains"]
    return taxonomy["skill_areas"]


def search_writing_skills(args: argparse.Namespace) -> int:
    catalog = load_writing_catalog()
    known_groups = {row["id"] for row in catalog["groups"]}
    if args.skill_group and args.skill_group not in known_groups:
        raise SystemExit(
            f"Unknown --skill-group {args.skill_group!r}; "
            f"choose from {', '.join(sorted(known_groups))}"
        )
    localized = localized_skill_labels(args.language)
    rows = [
        row
        for row in catalog["skills"]
        if (not args.skill_group or row["group"] == args.skill_group)
        and (not args.skill_slug or row["slug"] == args.skill_slug)
    ]
    ranked = [(writing_skill_score(row, args.query, localized), row) for row in rows]
    ranked = [(value, row) for value, row in ranked if value > 0]
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))
    selected = ranked[: args.limit]
    if args.json:
        payload = []
        for value, row in selected:
            enriched = {**row, "score": round(value, 3)}
            if row["id"] in localized:
                enriched["localized_interface"] = localized[row["id"]]
            payload.append(enriched)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for value, row in selected:
            label = localized.get(row["id"], {}).get("name", row["name"])
            print(f"{row['id']}  [{value:.1f}]  {label}")
            print(f"  {row['rhetorical_objective']}")
            print(f"  Example: {row['example']}")
            print(
                "  "
                f"group={row['group']} slug={row['slug']} "
                f"functions={','.join(row['related_phrase_functions'])}"
            )
            print(f"  Warning: {row['evidence_claim_warning']}")
            print(f"  Route: {row['canonical_en']}")
    return 0 if selected else 1


def search_patterns(args: argparse.Namespace) -> int:
    has_filter = any(
        (
            args.section,
            args.function,
            args.evidence,
            args.discipline,
            args.domain,
            args.skill_area,
            args.risk,
            args.max_claim_strength,
        )
    )
    if not args.query and not has_filter:
        raise SystemExit("Provide a query or at least one browse filter")
    ranked = [
        (score(row, args.query), row)
        for row in load_patterns()
        if compatible(row, args)
    ]
    ranked = [(value, row) for value, row in ranked if value > 0]
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))
    selected = ranked[: args.limit]

    if args.json:
        print(
            json.dumps(
                [{**row, "score": round(value, 3)} for value, row in selected],
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        for value, row in selected:
            print(f"{row['id']}  [{value:.1f}]  {row['title']}")
            print(f"  {row['template']}")
            print(
                "  "
                f"function={row['function']} stage={row['stage']} "
                f"evidence={row['evidence_requirement']} claim={row['claim_strength']} "
                f"risk={row['risk']} areas={','.join(row.get('skill_areas', []))}"
            )
    return 0 if selected else 1


def main() -> int:
    args = parser().parse_args()
    if args.limit < 1 or args.limit > 50:
        raise SystemExit("--limit must be between 1 and 50")
    listed = listing(args)
    if listed is not None:
        print(json.dumps(listed, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    writing_mode = args.writing_skills or args.skill_group or args.skill_slug
    if writing_mode:
        if not args.query and not args.skill_group and not args.skill_slug:
            raise SystemExit(
                "Provide a skill query, --skill-group, or --skill-slug with --writing-skills"
            )
        return search_writing_skills(args)
    return search_patterns(args)


if __name__ == "__main__":
    raise SystemExit(main())

