"""Fail when restricted academic source material is tracked by Git."""

from __future__ import annotations

from pathlib import PurePosixPath
import subprocess
import sys


WORKBOOK_SUFFIXES = {".xls", ".xlsx", ".xlsb", ".xlsm", ".ods", ".numbers"}
RESTRICTED_NAMES = {"academic_phrasebank_sections.xlsx"}


def main() -> int:
    output = subprocess.check_output(["git", "ls-files", "-z"])
    paths = [PurePosixPath(item.decode("utf-8")) for item in output.split(b"\0") if item]
    restricted = []
    for path in paths:
        private_tree = len(path.parts) >= 2 and path.parts[0].casefold() in {
            "data",
            "reports",
            "staging",
        } and path.parts[1].casefold() == "private"
        if (
            path.name.casefold() in RESTRICTED_NAMES
            or path.suffix.casefold() in WORKBOOK_SUFFIXES
            or private_tree
        ):
            restricted.append(path.as_posix())
    if restricted:
        for path in restricted:
            print(f"ERROR restricted source is tracked: {path}", file=sys.stderr)
        return 1
    print(f"tracked-file policy valid: {len(paths)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
