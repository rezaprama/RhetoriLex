"""Copy built public phrase data into the static Pages artifact."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "dist" / "phrases.json"
TARGET = ROOT / "docs" / "data" / "phrases.json"


def main() -> int:
    if not SOURCE.is_file():
        print(f"missing Pages data: {SOURCE.relative_to(ROOT)}", file=sys.stderr)
        return 1
    try:
        value = json.loads(SOURCE.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"invalid Pages data: {exc}", file=sys.stderr)
        return 1
    if not isinstance(value, (dict, list)):
        print("invalid Pages data: expected JSON object or array", file=sys.stderr)
        return 1
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    print(f"prepared {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
