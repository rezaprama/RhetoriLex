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
DEFAULT_ALIASES = ROOT / "data" / "taxonomy" / "search-aliases.v1.json"
DEFAULT_MANIFEST = ROOT / "data" / "canonical" / "catalog-manifest.v2.json"
DEFAULT_WRITING_SKILLS = ROOT / "data" / "editorial" / "writing-skills.v1.json"
DEFAULT_WRITING_SKILLS_ID = ROOT / "data" / "translations" / "writing-skills.id.v1.json"
RELEASE_VERSION = "0.2.0"
FORMAT_VERSION = "2.0.0"


def load_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def json_bytes(value: Any) -> bytes:
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    return (text + "\n").encode("utf-8")


def write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def public_entry(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "_line"}


def distribution_entry(
    source: dict[str, Any],
    taxonomy: dict[str, Any],
    aliases: dict[str, Any],
) -> dict[str, Any]:
    row = public_entry(source)
    function_name = row["function"]
    skill_areas = sorted(
        area["id"]
        for area in taxonomy["skill_areas"]
        if function_name in area["functions"]
    )
    entry_disciplines = set(row["disciplines"])
    if "general" in entry_disciplines:
        domains = ["general_academic"]
    else:
        domains = sorted(
            domain["id"]
            for domain in taxonomy["domains"]
            if entry_disciplines & set(domain["disciplines"])
        )
    search_aliases = set(aliases["function_aliases"].get(function_name, []))
    search_aliases.update(aliases["stage_aliases"].get(row["stage"], []))
    for discipline in row["disciplines"]:
        search_aliases.update(aliases["discipline_aliases"].get(discipline, []))
    for group in aliases["concept_groups"]:
        if function_name in group["functions"]:
            search_aliases.update(group["terms"])
    row["domains"] = domains
    row["skill_areas"] = skill_areas
    row["search_aliases"] = sorted(search_aliases, key=lambda value: value.casefold())
    return row


def catalog_document(
    entries: list[dict[str, Any]],
    taxonomy: dict[str, Any],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    public = [public_entry(row) for row in sorted(entries, key=lambda item: item["id"])]
    return {
        "format": "rhetorilex-catalog",
        "format_version": FORMAT_VERSION,
        "release_version": RELEASE_VERSION,
        "language": manifest["language"],
        "taxonomy_version": taxonomy["version"],
        "entry_count": len(public),
        "editorial": dict(manifest["editorial"]),
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
        "domains",
        "skill_areas",
        "search_aliases",
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
        for field_name in (
            "disciplines",
            "domains",
            "skill_areas",
            "search_aliases",
            "placeholders",
            "keywords",
        ):
            row[field_name] = "|".join(row[field_name])
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
        f"Release {RELEASE_VERSION}; format {FORMAT_VERSION}; taxonomy {taxonomy['version']}; "
        f"{len(entries)} original editorial templates.",
        "",
        "| ID | Function | Section | Skill areas | Template | Evidence | Claim | Risk |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in sorted(entries, key=lambda item: item["id"]):
        values = [
            row["id"],
            row["function"],
            row["stage"],
            ", ".join(row["skill_areas"]),
            row["template"],
            row["evidence_requirement"],
            row["claim_strength"],
            row["risk"],
        ]
        lines.append("| " + " | ".join(_markdown_cell(value) for value in values) + " |")
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
                domains_json TEXT NOT NULL,
                skill_areas_json TEXT NOT NULL,
                search_aliases_json TEXT NOT NULL,
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
        connection.execute("CREATE INDEX entries_stage_idx ON entries(stage)")
        connection.execute("CREATE INDEX entries_evidence_idx ON entries(evidence_requirement)")
        statement = "INSERT INTO entries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        for row in sorted(entries, key=lambda item: item["id"]):
            json_list = lambda value: json.dumps(
                value, ensure_ascii=False, separators=(",", ":")
            )
            connection.execute(
                statement,
                (
                    row["id"],
                    row["function"],
                    row["title"],
                    row["template"],
                    row["description"],
                    row["stage"],
                    json_list(row["disciplines"]),
                    json_list(row["domains"]),
                    json_list(row["skill_areas"]),
                    json_list(row["search_aliases"]),
                    row["claim_strength"],
                    row["evidence_requirement"],
                    int(row["causal_design_required"]),
                    json_list(row["placeholders"]),
                    json_list(row["keywords"]),
                    row["notes"],
                    row["risk"],
                    json.dumps(
                        row["provenance"],
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
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
    aliases_path: Path = DEFAULT_ALIASES,
    manifest_path: Path = DEFAULT_MANIFEST,
) -> list[Path]:
    canonical_entries, taxonomy, contract, errors = validate_paths(
        catalog_path, taxonomy_path, contract_path, aliases_path
    )
    if errors:
        raise ValueError("canonical data invalid:\n" + "\n".join(errors))
    aliases = load_json_object(aliases_path)
    manifest = load_json_object(manifest_path)
    writing_skills = load_json_object(DEFAULT_WRITING_SKILLS)
    writing_skills_id = load_json_object(DEFAULT_WRITING_SKILLS_ID)
    if manifest.get("release_version") != RELEASE_VERSION:
        raise ValueError("canonical manifest release version does not match builder")
    entries = [distribution_entry(row, taxonomy, aliases) for row in canonical_entries]
    if any(not row["skill_areas"] for row in entries):
        missing = [row["id"] for row in entries if not row["skill_areas"]]
        raise ValueError(f"entries without derived skill areas: {missing}")
    if any(not row["domains"] for row in entries):
        missing = [row["id"] for row in entries if not row["domains"]]
        raise ValueError(f"entries without derived domains: {missing}")

    dist.mkdir(parents=True, exist_ok=True)
    resources.mkdir(parents=True, exist_ok=True)
    skill_assets.mkdir(parents=True, exist_ok=True)
    catalog = catalog_document(entries, taxonomy, manifest)
    catalog_payload = json_bytes(catalog)
    outputs = [
        dist / "rhetorilex-v0.2.json",
        dist / "rhetorilex-v0.2.csv",
        dist / "rhetorilex-v0.2.sqlite3",
        dist / "rhetorilex-v0.2.md",
        dist / "phrases.json",
        dist / "writing-skills.json",
        dist / "writing-skills.id.json",
    ]
    write_bytes(outputs[0], catalog_payload)
    write_bytes(outputs[1], csv_document(entries))
    sqlite_document(outputs[2], entries)
    write_bytes(outputs[3], markdown_document(entries, taxonomy))
    write_bytes(outputs[4], catalog_payload)
    write_bytes(outputs[5], json_bytes(writing_skills))
    write_bytes(outputs[6], json_bytes(writing_skills_id))
    checksum_path = dist / "SHA256SUMS"
    write_bytes(checksum_path, checksums(outputs, dist))

    write_bytes(resources / "catalog.json", catalog_payload)
    write_bytes(resources / "phrases.json", catalog_payload)
    write_bytes(resources / "taxonomy.json", json_bytes(taxonomy))
    write_bytes(resources / "evidence_claim_contract.json", json_bytes(contract))
    write_bytes(resources / "search_aliases.json", json_bytes(aliases))
    write_bytes(resources / "canonical_manifest.json", json_bytes(manifest))
    write_bytes(resources / "writing_skills.json", json_bytes(writing_skills))
    write_bytes(resources / "writing_skills_id.json", json_bytes(writing_skills_id))
    write_bytes(skill_assets / "patterns.json", catalog_payload)
    write_bytes(skill_assets / "taxonomy.json", json_bytes(taxonomy))
    write_bytes(skill_assets / "search-aliases.json", json_bytes(aliases))
    write_bytes(skill_assets / "writing-skills.json", json_bytes(writing_skills))
    write_bytes(skill_assets / "writing-skills.id.json", json_bytes(writing_skills_id))

    stale_names = (
        "rhetorilex-v0.1.json",
        "rhetorilex-v0.1.csv",
        "rhetorilex-v0.1.sqlite3",
        "rhetorilex-v0.1.md",
    )
    for name in stale_names:
        stale = dist / name
        if stale.exists():
            stale.unlink()
    return outputs + [checksum_path]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--taxonomy", type=Path, default=DEFAULT_TAXONOMY)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--aliases", type=Path, default=DEFAULT_ALIASES)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--dist", type=Path, default=DEFAULT_DIST)
    parser.add_argument("--resources", type=Path, default=DEFAULT_RESOURCES)
    parser.add_argument("--skill-assets", type=Path, default=DEFAULT_SKILL_ASSETS)
    args = parser.parse_args(argv)
    try:
        outputs = build(
            args.catalog,
            args.taxonomy,
            args.contract,
            args.dist,
            args.resources,
            args.skill_assets,
            args.aliases,
            args.manifest,
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

