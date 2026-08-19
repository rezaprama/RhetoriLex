"""Command-line interface for RhetoriLex."""

from __future__ import annotations

import argparse
import json
from typing import Any, Sequence

from . import __version__
from .catalog import Catalog, Entry, SearchResult
from .contracts import check_entry_contract


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def _add_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--function", dest="function")
    parser.add_argument("--evidence")
    parser.add_argument("--max-claim-strength")
    parser.add_argument("--discipline")
    parser.add_argument("--stage", "--section", dest="stage")
    parser.add_argument("--risk", choices=("low", "medium", "high"))
    parser.add_argument("--domain")
    parser.add_argument("--skill-area")


def _filters(args: argparse.Namespace) -> dict[str, str | None]:
    return {
        "function": args.function,
        "evidence": args.evidence,
        "max_claim_strength": args.max_claim_strength,
        "discipline": args.discipline,
        "stage": args.stage,
        "risk": args.risk,
        "domain": args.domain,
        "skill_area": args.skill_area,
    }


def _print_result(result: SearchResult) -> None:
    print(f"{result.entry.id}  {result.entry.title}  [{result.score:.1f} {result.match}]")
    print(f"  {result.entry.template}")
    print(
        f"  function={result.entry.function} stage={result.entry.stage} "
        f"evidence={result.entry.evidence_requirement} strength={result.entry.claim_strength} "
        f"risk={result.entry.risk} areas={','.join(result.entry.skill_areas)}"
    )


def _print_entry(entry: Entry) -> None:
    print(f"{entry.id}  {entry.title}")
    print(entry.template)
    print(f"Use: {entry.description}")
    print(
        f"Function: {entry.function} | stage: {entry.stage} | "
        f"evidence: {entry.evidence_requirement} | claim: {entry.claim_strength} | risk: {entry.risk}"
    )
    print(f"Skill areas: {', '.join(entry.skill_areas)}")
    print(f"Domains: {', '.join(entry.domains)}")
    print(f"Notes: {entry.notes}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rhetorilex", description=__doc__)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    commands = parser.add_subparsers(dest="command", required=True)

    search = commands.add_parser("search", help="rank templates for a writing need")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--no-fuzzy", action="store_true")
    _add_filters(search)

    browse = commands.add_parser("browse", help="browse templates by paper section or semantic facet")
    browse.add_argument("--limit", type=int, default=25)
    _add_filters(browse)

    suggest = commands.add_parser("suggest", help="complete moves, titles, keywords, and aliases")
    suggest.add_argument("prefix")
    suggest.add_argument("--limit", type=int, default=8)

    explain = commands.add_parser("explain", help="show use guidance and contract status")
    explain.add_argument("id")

    inspect = commands.add_parser("inspect", help="show catalog health and facet distribution")
    inspect.add_argument("--validate", action="store_true")

    taxonomy = commands.add_parser("taxonomy", help="show stable semantic taxonomy")
    taxonomy.add_argument("section", nargs="?")

    random_parser = commands.add_parser("random", help="choose a template, optionally reproducibly")
    random_parser.add_argument("--seed")
    _add_filters(random_parser)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        catalog = Catalog.load()
        if args.command == "search":
            results = catalog.search(
                args.query,
                limit=args.limit,
                fuzzy=not args.no_fuzzy,
                **_filters(args),
            )
            if args.json:
                print(_json([item.as_dict() for item in results]))
            else:
                for result in results:
                    _print_result(result)
            return 0 if results else 1

        if args.command == "browse":
            entries = catalog.browse(limit=args.limit, **_filters(args))
            if args.json:
                print(_json([entry.as_dict() for entry in entries]))
            else:
                for entry in entries:
                    _print_entry(entry)
                    print()
            return 0 if entries else 1

        if args.command == "suggest":
            suggestions = catalog.suggest(args.prefix, limit=args.limit)
            print(_json(suggestions) if args.json else "\n".join(suggestions))
            return 0 if suggestions else 1

        if args.command == "explain":
            entry = catalog.get(args.id)
            issues = [
                {"code": issue.code, "message": issue.message, "severity": issue.severity}
                for issue in check_entry_contract(entry, catalog.contract)
            ]
            if args.json:
                value = entry.as_dict()
                value["contract_issues"] = issues
                print(_json(value))
            else:
                _print_entry(entry)
                print("Contract: valid" if not issues else f"Contract: {len(issues)} issue(s)")
            return 0 if not issues else 2

        if args.command == "inspect":
            value = catalog.counts()
            if args.validate:
                failures = {
                    entry.id: [issue.message for issue in check_entry_contract(entry, catalog.contract)]
                    for entry in catalog.entries
                    if check_entry_contract(entry, catalog.contract)
                }
                value["contract_failures"] = failures
                value["valid"] = not failures
            print(_json(value))
            return 0 if value.get("valid", True) else 2

        if args.command == "taxonomy":
            value = catalog.taxonomy
            if args.section:
                if args.section not in value:
                    parser.error(f"unknown taxonomy section: {args.section}")
                value = value[args.section]
            print(_json(value))
            return 0

        if args.command == "random":
            entry = catalog.random(seed=args.seed, **_filters(args))
            print(_json(entry.as_dict()) if args.json else entry.template)
            return 0
    except (KeyError, LookupError, ValueError) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())