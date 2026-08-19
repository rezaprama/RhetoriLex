#!/usr/bin/env python3
"""Search RhetoriLex's bundled clean-room patterns without dependencies."""

from __future__ import annotations

import argparse
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
from typing import Any


TOKEN_RE = re.compile(r"[a-z0-9]+")
STRENGTH = {"tentative": 0, "bounded": 1, "assertive": 2, "causal": 3}


def tokens(value: str) -> set[str]:
    return set(TOKEN_RE.findall(value.casefold()))


def load_patterns() -> list[dict[str, Any]]:
    path = Path(__file__).resolve().parents[1] / "assets" / "patterns.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload if isinstance(payload, list) else payload.get("entries", [])
    if not records:
        raise SystemExit(f"No patterns found in {path}")
    return records


def compatible(row: dict[str, Any], args: argparse.Namespace) -> bool:
    if args.function and row["function"] != args.function:
        return False
    if args.section and row["stage"] not in {args.section, "general"}:
        return False
    if args.evidence and row["evidence_requirement"] != args.evidence:
        return False
    if args.discipline and args.discipline not in row["disciplines"] and "general" not in row["disciplines"]:
        return False
    if args.risk and row["risk"] != args.risk:
        return False
    if args.max_claim_strength and STRENGTH[row["claim_strength"]] > STRENGTH[args.max_claim_strength]:
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
    ]
    haystack = " ".join(fields).casefold()
    query_tokens = tokens(query)
    overlap = len(query_tokens & tokens(haystack))
    lexical = 60 * overlap / max(1, len(query_tokens))
    phrase = 20 if query.casefold().strip() in haystack else 0
    fuzzy = max(SequenceMatcher(None, query.casefold(), value.casefold()).ratio() for value in fields) * 20
    return lexical + phrase + fuzzy


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("query", help="writing intent, such as 'cautious interpretation'")
    result.add_argument("--section", "--stage", dest="section")
    result.add_argument("--function")
    result.add_argument("--evidence")
    result.add_argument("--max-claim-strength", choices=tuple(STRENGTH))
    result.add_argument("--discipline")
    result.add_argument("--risk", choices=("low", "medium", "high"))
    result.add_argument("--limit", type=int, default=3)
    result.add_argument("--json", action="store_true")
    return result


def main() -> int:
    args = parser().parse_args()
    if args.limit < 1 or args.limit > 20:
        raise SystemExit("--limit must be between 1 and 20")
    ranked = [
        (score(row, args.query), row)
        for row in load_patterns()
        if compatible(row, args)
    ]
    ranked = [(value, row) for value, row in ranked if value > 0]
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))
    selected = ranked[: args.limit]

    if args.json:
        print(json.dumps([{**row, "score": round(value, 3)} for value, row in selected], indent=2, ensure_ascii=False))
    else:
        for value, row in selected:
            print(f"{row['id']}  [{value:.1f}]  {row['title']}")
            print(f"  {row['template']}")
            print(
                "  "
                f"function={row['function']} stage={row['stage']} "
                f"evidence={row['evidence_requirement']} claim={row['claim_strength']} risk={row['risk']}"
            )
    return 0 if selected else 1


if __name__ == "__main__":
    raise SystemExit(main())
