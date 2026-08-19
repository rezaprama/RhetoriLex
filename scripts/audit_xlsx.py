#!/usr/bin/env python3
"""Audit an XLSX container without emitting workbook text.

This utility intentionally reports structure and aggregate quality signals only.
It does not write to, export, or execute the input workbook.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import unicodedata
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable
from xml.etree import ElementTree as ET


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CELL_RE = re.compile(r"^([A-Z]+)(\d+)$")
SPLIT_RE = re.compile(r"\r\n|\r|\n| / ")
ELLIPSIS_RE = re.compile(r"(?:\.\.\.|…)$")
MAX_ARCHIVE_BYTES = 50 * 1024 * 1024
MAX_MEMBER_BYTES = 12 * 1024 * 1024


@dataclass(frozen=True)
class Cell:
    address: str
    value: str
    has_formula: bool


@dataclass(frozen=True)
class Sheet:
    name: str
    dimension: str
    cells: tuple[Cell, ...]


def _safe_xml(archive: zipfile.ZipFile, name: str) -> ET.Element:
    info = archive.getinfo(name)
    if info.file_size > MAX_MEMBER_BYTES:
        raise ValueError(f"Refusing oversized XML member: {name}")
    return ET.fromstring(archive.read(name))


def _validate_archive(archive: zipfile.ZipFile) -> None:
    total = 0
    for info in archive.infolist():
        path = PurePosixPath(info.filename)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("Unsafe path in XLSX container")
        total += info.file_size
    if total > MAX_ARCHIVE_BYTES:
        raise ValueError("Refusing XLSX with excessive uncompressed size")


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    name = "xl/sharedStrings.xml"
    if name not in archive.namelist():
        return []
    root = _safe_xml(archive, name)
    return ["".join(node.text or "" for node in item.findall(f".//{{{MAIN_NS}}}t")) for item in root]


def _relationship_targets(archive: zipfile.ZipFile) -> dict[str, str]:
    root = _safe_xml(archive, "xl/_rels/workbook.xml.rels")
    targets: dict[str, str] = {}
    for relation in root.findall(f"{{{PKG_REL_NS}}}Relationship"):
        relation_id = relation.attrib.get("Id", "")
        target = relation.attrib.get("Target", "")
        if target.startswith("/"):
            target = target.lstrip("/")
        elif not target.startswith("xl/"):
            target = str(PurePosixPath("xl") / target)
        targets[relation_id] = str(PurePosixPath(target))
    return targets


def _cell_text(cell: ET.Element, shared: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(f".//{{{MAIN_NS}}}t"))
    value = cell.findtext(f"{{{MAIN_NS}}}v", default="")
    if cell_type == "s" and value:
        index = int(value)
        return shared[index] if 0 <= index < len(shared) else ""
    return value


def read_workbook(path: Path) -> tuple[Sheet, ...]:
    with zipfile.ZipFile(path) as archive:
        _validate_archive(archive)
        shared = _shared_strings(archive)
        targets = _relationship_targets(archive)
        workbook = _safe_xml(archive, "xl/workbook.xml")
        sheets: list[Sheet] = []
        for item in workbook.findall(f".//{{{MAIN_NS}}}sheet"):
            name = item.attrib.get("name", "Unnamed")
            relation_id = item.attrib.get(f"{{{REL_NS}}}id", "")
            target = targets.get(relation_id)
            if not target or target not in archive.namelist():
                continue
            root = _safe_xml(archive, target)
            dimension = root.find(f"{{{MAIN_NS}}}dimension")
            dimension_ref = dimension.attrib.get("ref", "") if dimension is not None else ""
            cells: list[Cell] = []
            for node in root.findall(f".//{{{MAIN_NS}}}c"):
                address = node.attrib.get("r", "")
                value = _cell_text(node, shared)
                if value != "":
                    cells.append(Cell(address, value, node.find(f"{{{MAIN_NS}}}f") is not None))
            sheets.append(Sheet(name, dimension_ref, tuple(cells)))
    return tuple(sheets)


def _column(address: str) -> str:
    match = CELL_RE.match(address)
    return match.group(1) if match else ""


def _normalize(text: str) -> str:
    folded = unicodedata.normalize("NFKC", text).translate(
        str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-"})
    )
    return " ".join(folded.split()).casefold()


def _candidate_cells(sheets: Iterable[Sheet], payload_column: str) -> list[tuple[str, Cell]]:
    candidates: list[tuple[str, Cell]] = []
    for sheet in sheets:
        for cell in sheet.cells:
            text = cell.value.strip()
            if _column(cell.address) != payload_column:
                continue
            if "\n" in text or "\r" in text or " / " in text or ELLIPSIS_RE.search(text):
                candidates.append((sheet.name, cell))
    return candidates


def audit(path: Path, payload_column: str = "C") -> dict[str, object]:
    sheets = read_workbook(path)
    candidates = _candidate_cells(sheets, payload_column.upper())
    segments: list[tuple[str, str, str]] = []
    newline_units = 0
    slash_occurrences = 0
    slash_cells = 0
    for sheet_name, cell in candidates:
        text = cell.value.strip()
        newline_parts = [part.strip() for part in re.split(r"\r\n|\r|\n", text) if part.strip()]
        newline_units += len(newline_parts)
        count = text.count(" / ")
        slash_occurrences += count
        slash_cells += int(count > 0)
        for index, segment in enumerate(part.strip() for part in SPLIT_RE.split(text) if part.strip()):
            segments.append((sheet_name, f"{cell.address}:{index}", segment))

    exact_counts = Counter(segment for _, _, segment in segments)
    normalized_counts = Counter(_normalize(segment) for _, _, segment in segments)
    category_sizes = []
    for _, cell in candidates:
        category_sizes.append(len([part for part in SPLIT_RE.split(cell.value) if part.strip()]))

    summary: dict[str, object] = {
        "file": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
        "worksheets": [
            {
                "name": sheet.name,
                "dimension": sheet.dimension,
                "nonempty_cells": len(sheet.cells),
                "formula_cells": sum(cell.has_formula for cell in sheet.cells),
            }
            for sheet in sheets
        ],
        "totals": {
            "worksheets": len(sheets),
            "nonempty_cells": sum(len(sheet.cells) for sheet in sheets),
            "formula_cells": sum(cell.has_formula for sheet in sheets for cell in sheet.cells),
            "payload_cells": len(candidates),
            "newline_units": newline_units,
            "combined_delimiter_units": len(segments),
            "literal_space_slash_space_cells": slash_cells,
            "literal_space_slash_space_occurrences": slash_occurrences,
        },
        "duplicates": {
            "exact_unique": len(exact_counts),
            "exact_groups": sum(count > 1 for count in exact_counts.values()),
            "exact_extras": sum(count - 1 for count in exact_counts.values() if count > 1),
            "normalized_unique": len(normalized_counts),
            "normalized_groups": sum(count > 1 for count in normalized_counts.values()),
            "normalized_extras": sum(count - 1 for count in normalized_counts.values() if count > 1),
        },
        "format_signals": {
            "terminal_ellipsis": sum(bool(ELLIPSIS_RE.search(segment)) for _, _, segment in segments),
            "starts_uppercase": sum(segment[:1].isupper() for _, _, segment in segments),
            "leading_or_trailing_whitespace": sum(segment != segment.strip() for _, _, segment in segments),
            "space_before_punctuation": sum(bool(re.search(r"\s+[,;:?!]", segment)) for _, _, segment in segments),
        },
        "taxonomy_shape": {
            "categories": len(category_sizes),
            "minimum_units": min(category_sizes, default=0),
            "maximum_units": max(category_sizes, default=0),
            "mean_units": round(statistics.mean(category_sizes), 4) if category_sizes else 0,
            "median_units": statistics.median(category_sizes) if category_sizes else 0,
            "singleton_categories": sum(size == 1 for size in category_sizes),
        },
        "release_decision": "exclude_source_and_promote_zero_entries",
    }
    return summary


def to_markdown(summary: dict[str, object]) -> str:
    totals = summary["totals"]
    duplicates = summary["duplicates"]
    taxonomy = summary["taxonomy_shape"]
    sheet_lines = "\n".join(
        f"- `{sheet['name']}`: `{sheet['dimension']}`, {sheet['nonempty_cells']} non-empty cells, {sheet['formula_cells']} formulas"
        for sheet in summary["worksheets"]
    )
    return f"""# XLSX Aggregate Audit

Source hash: `{summary['sha256']}`

## Structure

{sheet_lines}

- Payload cells: {totals['payload_cells']}
- Newline-only units: {totals['newline_units']}
- Combined newline and literal ` / ` units: {totals['combined_delimiter_units']}
- Literal ` / ` occurrences: {totals['literal_space_slash_space_occurrences']} across {totals['literal_space_slash_space_cells']} cells

## Duplicate signals

- Exact: {duplicates['exact_unique']} unique; {duplicates['exact_groups']} duplicate group; {duplicates['exact_extras']} extra occurrence
- Normalized: {duplicates['normalized_unique']} unique; {duplicates['normalized_groups']} duplicate group; {duplicates['normalized_extras']} extra occurrence

## Taxonomy shape

- Categories: {taxonomy['categories']}
- Size: {taxonomy['minimum_units']} to {taxonomy['maximum_units']}; median {taxonomy['median_units']}; mean {taxonomy['mean_units']}
- Singleton categories: {taxonomy['singleton_categories']}

## Decision

No workbook wording is reproduced in this report. Zero entries are eligible for public release. Build the public dataset independently.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--payload-column", default="C")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    summary = audit(args.input, args.payload_column)
    rendered = json.dumps(summary, indent=2, ensure_ascii=False) + "\n" if args.format == "json" else to_markdown(summary)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
