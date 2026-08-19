#!/usr/bin/env python3
"""Quarantine XLSX candidates for authorized private review.

This command never promotes records into the public dataset. It requires a
written authorization marker and restricts output to an explicitly named
private staging root. Do not use it to bypass source licenses or notices.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from audit_xlsx import ELLIPSIS_RE, SPLIT_RE, _candidate_cells, read_workbook


AUTHORIZATION_MARKER = "AUTHORIZED_FOR_PRIVATE_ACADEMIC_MIGRATION"
PUBLIC_COMPONENTS = {"canonical", "dist", "docs", "skills", "src"}


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def _validate_paths(output: Path, private_root: Path) -> tuple[Path, Path]:
    root = private_root.resolve()
    target = output.resolve()
    if not _inside(target, root):
        raise ValueError("Output must remain inside --private-root")
    if any(part.casefold() in PUBLIC_COMPONENTS for part in target.parts):
        raise ValueError("Output path overlaps a public release component")
    return target, root


def _authorization(path: Path) -> None:
    if not path.is_file() or path.read_text(encoding="utf-8").strip() != AUTHORIZATION_MARKER:
        raise PermissionError(
            "Migration requires a file containing exactly "
            f"{AUTHORIZATION_MARKER}. This marker records workflow authorization; "
            "it does not replace permission from the rights holder."
        )


def migrate(input_path: Path, output: Path, private_root: Path, payload_column: str) -> dict[str, object]:
    target, root = _validate_paths(output, private_root)
    source_hash = hashlib.sha256(input_path.read_bytes()).hexdigest()
    sheets = read_workbook(input_path)
    candidate_cells = _candidate_cells(sheets, payload_column.upper())
    records: list[dict[str, object]] = []

    for sheet_name, cell in candidate_cells:
        parts = [part.strip() for part in SPLIT_RE.split(cell.value) if part.strip()]
        for position, original in enumerate(parts):
            digest = hashlib.sha256(
                f"{source_hash}\x00{sheet_name}\x00{cell.address}\x00{position}\x00{original}".encode("utf-8")
            ).hexdigest()[:20]
            records.append(
                {
                    "candidate_id": f"private.{digest}",
                    "source_sha256": source_hash,
                    "sheet": sheet_name,
                    "cell": cell.address,
                    "position": position,
                    "original_text": original,
                    "signals": {
                        "terminal_ellipsis": bool(ELLIPSIS_RE.search(original)),
                        "word_count": len(re.findall(r"\b\w+\b", original)),
                    },
                    "provenance_status": "unresolved",
                    "review_status": "private_quarantine",
                    "release_eligible": False,
                }
            )

    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    return {
        "input_sha256": source_hash,
        "private_root": str(root),
        "output": str(target),
        "quarantined_candidates": len(records),
        "publicly_promoted": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--private-root", type=Path, required=True)
    parser.add_argument("--authorization-file", type=Path, required=True)
    parser.add_argument("--payload-column", default="C")
    args = parser.parse_args()

    _authorization(args.authorization_file)
    result = migrate(args.input, args.output, args.private_root, args.payload_column)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
