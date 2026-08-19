"""Build deterministic RhetoriLex distribution and package resources."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import sys
from typing import Any

from validate_data import DEFAULT_CATALOG, DEFAULT_CONTRACT, DEFAULT_TAXONOMY, validate_paths


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIST = ROOT / "data" / "dist"
DEFAULT_RESOURCES = ROOT / "src" / "rhetorilex" / "resources"
DEFAULT_SKILL_ASSETS = ROOT / "skills" / "rhetorilex" / "assets"
FORMAT_VERSION = "1.0.0"


def json_bytes(value: Any) -> bytes:
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    return (text + "\n").encode("utf-8")


def write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def public_entry(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "_line"}


def catalog_document(entries: list[dict[str, Any]], taxonomy: dict[str, Any]) -> dict[str, Any]:
    public = [public_entry(row) for row in sorted(entries, key=lambda item: item["id"])]
    return {
        "format": "rhetorilex-catalog",
        "format_version": FORMAT_VERSION,
        "taxonomy_version": taxonomy["version"],
        "entry_count": len(public),
        "entries": public,
    }


def csv_document(entries: list[dict[str, Any]]) -> bytes:
    fields = [
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
        "provenance_method",
        "provenance_author",
        "source_reuse",
        "version",
    ]
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for source in sorted(entries, key=lambda item: item["id"]):
        row = public_entry(source)
        provenance = row.pop("provenance")
        row["disciplines"] = "|".join(row["disciplines"])
        row["placeholders"] = "|".join(row["placeholders"])
        row["keywords"] = "|".join(row["keywords"])
        row["causal_design_required"] = str(row["causal_design_required"]).lower()
        row["provenance_method"] = provenance["method"]
        row["provenance_author"] = provenance["author"]
        row["source_reuse"] = str(provenance["source_reuse"]).lower()
        writer.writerow(row)
    return buffer.getvalue().encode("utf-8")


def _markdown_cell(text: Any) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def markdown_document(entries: list[dict[str, Any]], taxonomy: dict[str, Any]) -> bytes:
    lines = [
        "# RhetoriLex Catalog",
        "",
        f"Format {FORMAT_VERSION}; taxonomy {taxonomy['version']}; {len(entries)} original editorial templates.",
        "",
        "| ID | Function | Template | Evidence | Claim | Risk |",
        "|---|---|---|---|---|---|",
    ]
    for row in sorted(entries, key=lambda item: item["id"]):
        lines.append(
            "| "
            + " | ".join(
                _markdown_cell(row[key])
                for key in ("id", "function", "template", "evidence_requirement", "claim_strength", "risk")
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines).encode("utf-8")


def sqlite_document(path: Path, entries: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    connection = sqlite3.connect(path)
    try:
        connection.execute("PRAGMA page_size = 4096")
        connection.execute("PRAGMA journal_mode = DELETE")
        connection.execute("PRAGMA synchronous = FULL")
        connection.execute(
            """
            CREATE TABLE entries (
                id TEXT PRIMARY KEY,
                function TEXT NOT NULL,
                title TEXT NOT NULL,
                template TEXT NOT NULL,
                description TEXT NOT NULL,
                stage TEXT NOT NULL,
                disciplines_json TEXT NOT NULL,
                claim_strength TEXT NOT NULL,
                evidence_requirement TEXT NOT NULL,
                causal_design_required INTEGER NOT NULL CHECK (causal_design_required IN (0, 1)),
                placeholders_json TEXT NOT NULL,
                keywords_json TEXT NOT NULL,
                notes TEXT NOT NULL,
                risk TEXT NOT NULL,
                provenance_json TEXT NOT NULL,
                version INTEGER NOT NULL
            ) WITHOUT ROWID
            """
        )
        connection.execute("CREATE INDEX entries_function_idx ON entries(function)")
        connection.execute("CREATE INDEX entries_evidence_idx ON entries(evidence_requirement)")
        statement = "INSERT INTO entries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        for source in sorted(entries, key=lambda item: item["id"]):
            row = public_entry(source)
            connection.execute(
                statement,
                (
                    row["id"],
                    row["function"],
                    row["title"],
                    row["template"],
                    row["description"],
                    row["stage"],
                    json.dumps(row["disciplines"], ensure_ascii=False, separators=(",", ":")),
                    row["claim_strength"],
                    row["evidence_requirement"],
                    int(row["causal_design_required"]),
                    json.dumps(row["placeholders"], ensure_ascii=False, separators=(",", ":")),
                    json.dumps(row["keywords"], ensure_ascii=False, separators=(",", ":")),
                    row["notes"],
                    row["risk"],
                    json.dumps(row["provenance"], ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                    row["version"],
                ),
            )
        connection.commit()
        connection.execute("VACUUM")
    finally:
        connection.close()


def checksums(paths: list[Path], base: Path) -> bytes:
    lines = []
    for path in sorted(paths, key=lambda item: item.name):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(base).as_posix()}")
    return ("\n".join(lines) + "\n").encode("ascii")


def build(
    catalog_path: Path = DEFAULT_CATALOG,
    taxonomy_path: Path = DEFAULT_TAXONOMY,
    contract_path: Path = DEFAULT_CONTRACT,
    dist: Path = DEFAULT_DIST,
    resources: Path = DEFAULT_RESOURCES,
    skill_assets: Path = DEFAULT_SKILL_ASSETS,
) -> list[Path]:
    entries, taxonomy, contract, errors = validate_paths(catalog_path, taxonomy_path, contract_path)
    if errors:
        raise ValueError("canonical data invalid:\n" + "\n".join(errors))
    dist.mkdir(parents=True, exist_ok=True)
    resources.mkdir(parents=True, exist_ok=True)
    skill_assets.mkdir(parents=True, exist_ok=True)

    catalog = catalog_document(entries, taxonomy)
    catalog_payload = json_bytes(catalog)
    outputs = [
        dist / "rhetorilex-v0.1.json",
        dist / "rhetorilex-v0.1.csv",
        dist / "rhetorilex-v0.1.sqlite3",
        dist / "rhetorilex-v0.1.md",
        dist / "phrases.json",
    ]
    write_bytes(outputs[0], catalog_payload)
    write_bytes(outputs[1], csv_document(entries))
    sqlite_document(outputs[2], entries)
    write_bytes(outputs[3], markdown_document(entries, taxonomy))
    write_bytes(outputs[4], catalog_payload)
    checksum_path = dist / "SHA256SUMS"
    write_bytes(checksum_path, checksums(outputs, dist))

    write_bytes(resources / "catalog.json", catalog_payload)
    write_bytes(resources / "phrases.json", catalog_payload)
    write_bytes(resources / "taxonomy.json", json_bytes(taxonomy))
    write_bytes(resources / "evidence_claim_contract.json", json_bytes(contract))
    write_bytes(skill_assets / "patterns.json", catalog_payload)
    return outputs + [checksum_path]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--taxonomy", type=Path, default=DEFAULT_TAXONOMY)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--resources", type=Path, default=DEFAULT_RESOURCES)
    parser.add_argument("--skill-assets", type=Path, default=DEFAULT_SKILL_ASSETS)
    args = parser.parse_args(argv)
    try:
        outputs = build(
            args.catalog, args.taxonomy, args.contract, args.dist, args.resources, args.skill_assets
        )
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error) as exc:
        print(f"build failed: {exc}", file=sys.stderr)
        return 1
    for output in outputs:
        try:
            label = output.relative_to(ROOT)
        except ValueError:
            label = output
        print(label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
